# main.py
import uvicorn
from fastapi import FastAPI, Query, Body, HTTPException  # FastAPI import
from pydantic import BaseModel
import asyncpg # type: ignore

app = FastAPI()

DATABASE_URL="postgres://postgres.qevaccqpeahkommhvhbs:26yF1DY3oWmHrgZM@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres"
# 데이터베이스 연결을 위한 비동기 함수
async def connect_to_db():
    return await asyncpg.connect(DATABASE_URL)

@app.get("/analysis")
async def analysis(name: str = Query, age: str = Query, body = Body(...)):
		conn = await connect_to_db()
		try:
			# 데이터베이스 쿼리 실행
			query = "SELECT * FROM todos;"
			# query = "UPDATE todos SET is_complete = true WHERE id=17"
			result = await conn.fetch(query)

			# 결과 반환
			return {"data": result}
		
		except Exception as e:
			# 쿼리 실패 시 HTTPException을 발생시킵니다.
			raise HTTPException(status_code=500, detail=str(e))

		finally:
			# 데이터베이스 연결을 닫습니다.
			await conn.close()
		print('name: {}'.format(name))
		print('age: {}'.format(age))
		print('body: {}'.format(body))
		return 'success'
 
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
