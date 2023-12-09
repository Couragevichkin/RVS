import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Numbers as SchemaNumbers

from schema import Numbers

from model import Numbers as ModelNumber

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URI'])
print(os.environ['DATABASE_URI'])

@app.post('/number/', response_model=SchemaNumbers)
async def number(number: SchemaNumbers):
    db_number = ModelNumber(number = number.number)
    first_check = db.session.query(ModelNumber).filter(ModelNumber.number==number.number).all()
    if len(first_check) == 0:
        second_check = db.session.query(ModelNumber).filter(ModelNumber.number==number.number+1).all()
        if len(second_check) == 0:
            db_number.number += 1
            db.session.add(db_number)
            db.session.commit()
        else:
            raise HTTPException(
            status_code=406, detail=f"Number {db_number.number} + 1 already is in database"
        )
    else:
        raise HTTPException(
            status_code=406, detail=f"Number {db_number.number} already is in database"
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"number {db_number.number} was written in db")


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)