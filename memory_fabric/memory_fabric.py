import time
import os
import json
import math

from collections import deque

import psycopg2
import redis

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---- MicroMemory (ephemeral, shared via Redis) ----

class MicroMemory:
    def __init__(self, redis_url="redis://localhost:6379/0", prefix="micro:", max_items=200):
        self.r = redis.StrictRedis.from_url(redis_url)
        self.prefix = prefix
        self.max_items = max_items

    def add(self, user_id, text):
        key = f"{self.prefix}{user_id}"
        item = json.dumps({'text': text, 'ts': time.time()})
        self.r.lpush(key, item)
        self.r.ltrim(key, 0, self.max_items - 1)

    def get_all(self, user_id):
        key = f"{self.prefix}{user_id}"
        items = self.r.lrange(key, 0, self.max_items - 1)
        return [json.loads(i)['text'] for i in items]

# ---- MesoMemory (persistent, cloud-ready: PostgreSQL) ----

class MesoMemory:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)
        self._init_table()

    def _init_table(self):
        with self.conn:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR,
                    summary TEXT,
                    created_at DOUBLE PRECISION,
                    last_access DOUBLE PRECISION
                )
            """)

    def add_summary(self, user_id, summary):
        now = time.time()
        with self.conn:
            self.conn.cursor().execute(
                "INSERT INTO summaries (user_id, summary, created_at, last_access) VALUES (%s, %s, %s, %s)",
                (user_id, summary, now, now)
            )

    def fetch_top(self, user_id, limit=5):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT summary FROM summaries WHERE user_id=%s ORDER BY last_access DESC, created_at DESC LIMIT %s",
                (user_id, limit)
            )
            rows = cur.fetchall()
            # Optionally update last_access here
        return [r[0] for r in rows]

# ---- MacroMemory (FAISS, vector DB, per user; scalable!) ----

class MacroMemory:
    def __init__(self, user_id, dim=768, index_dir="./vector_index"):
        self.user_id = user_id
        self.emb_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = dim
        self.index_path = f"{index_dir}/{user_id}.index"
        self.meta_path = f"{index_dir}/{user_id}_meta.json"
        self.index = faiss.read_index(self.index_path) if os.path.exists(self.index_path) else faiss.IndexFlatIP(dim)
        self.meta = json.load(open(self.meta_path)) if os.path.exists(self.meta_path) else []

    def add(self, text, importance=1.0):
        emb = self.emb_model.encode([text])
        faiss.normalize_L2(emb)
        self.index.add(np.array(emb, dtype='float32'))
        self.meta.append({'text': text, 'ts': time.time(), 'importance': importance})
        self.save()

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            json.dump(self.meta, f)

    def query(self, q, k=5):
        q_emb = self.emb_model.encode([q]).astype('float32')
        faiss.normalize_L2(q_emb)
        dists, idxs = self.index.search(q_emb, k)
        results = []
        for dist, idx in zip(dists[0], idxs[0]):
            if idx < len(self.meta):
                m = self.meta[idx]
                score = dist * m['importance']
                results.append((m['text'], score))
        return sorted(results, key=lambda x: -x[1])

    def decay_importance(self, half_life_hours=48):
        now = time.time()
        λ = math.log(2) / (half_life_hours * 3600)
        for m in self.meta:
            age = now - m['ts']
            m['importance'] *= math.exp(-λ * age)
        self.save()

# ---- MemoryFabric: orchestrator ----

class MemoryFabric:
    def __init__(self, redis_url, pg_dsn, vector_index_dir="./vector_index"):
        self.micro = MicroMemory(redis_url)
        self.meso = MesoMemory(pg_dsn)
        self.vector_index_dir = vector_index_dir

    def macro(self, user_id):
        return MacroMemory(user_id, index_dir=self.vector_index_dir)

    def add_interaction(self, user_id, text, significance):
        self.micro.add(user_id, text)
        if significance > 0.7:
            self.macro(user_id).add(text, importance=significance)
        # Example: summarize and store to meso if micro buffer hits max
        if len(self.micro.get_all(user_id)) == self.micro.max_items:
            old = self.micro.get_all(user_id)[-1]
            summary = self.generate_summary([old])  # Wire to GPT/local LLM!
            self.meso.add_summary(user_id, summary)

    def retrieve_context(self, user_id, query):
        micro_ctx = self.micro.get_all(user_id)
        meso_ctx = self.meso.fetch_top(user_id)
        macro_hits = [t for t, _ in self.macro(user_id).query(query)]
        return micro_ctx, meso_ctx, macro_hits

    def generate_summary(self, texts):
        # Placeholder for GPT/local LLM summarization
        return " | ".join(texts)

# ---- Example usage (production: wire this to FastAPI endpoints) ----

# from fastapi import FastAPI, Depends
# app = FastAPI()
# fabric = MemoryFabric(redis_url="redis://localhost:6379/0", pg_dsn="postgresql://user:pass@host/db")
#
# @app.post("/memories")
# async def add_memory(req: dict, user_id: str = Depends(get_user)):
#     fabric.add_interaction(user_id, req['text'], req['significance'])
#     return {"status": "ok"}
#
# @app.get("/context")
# async def get_context(q: str, user_id: str = Depends(get_user)):
#     micro, meso, macro = fabric.retrieve_context(user_id, q)
#     return {"micro": micro, "meso": meso, "macro": macro}

