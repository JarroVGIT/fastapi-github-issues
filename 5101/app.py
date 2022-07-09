import asyncio
from fastapi import FastAPI, WebSocket
from time import sleep

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self,id: str,websocket: WebSocket):
        await websocket.accept()
        self.connections[id] = websocket
    
    async def disconnect(self, id: str):
        if id in self.connections:
            await self.connections[id].close(code=100,reason=None)
            del self.connections[id]

    async def send_response(self,id: str,data: str,status:str='running'):
        print(f"Tries to send response for client with id :{id}. Response is {data}")
        try:
            await self.connections[id].send_json(
                data=dict(timestamp="whatever",message=data,id=id,status=status)
            )
            if status=="completed":
                await self.disconnect(id)
        except Exception as e:
            print(str(e))
            await self.disconnect(id)

manager = ConnectionManager()#create a context for web socket manager

@app.websocket("/auto_algo/{client_id}")
async def auto_algo(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    await automate_algorithm(idt=client_id)

async def send_message_to_socket(client_id: str, what: str, status:str='running'):
    global manager
    await manager.send_response(client_id, what,status)

def sync_function(idt: str, mapper:bool=False):
    sleep(1)
    return

# automate to algorithm ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def automate_algorithm(idt,language='en'):
    
    await  send_message_to_socket(client_id=idt,what="process starting")#This message appear at start correctly
    await asyncio.sleep(0)

    mds2 = sync_function(idt,mapper=False)
    await  send_message_to_socket(client_id=idt,what="main_data_structure 2 created...")#the rest of message appear together at the end of process
    await asyncio.sleep(0)

    sample_data = sync_function(idt,mapper=False)
    await  send_message_to_socket(client_id=idt,what="sample data created...")
    await asyncio.sleep(0)

    corr = sync_function(idt,mapper=False)
    await  send_message_to_socket(client_id=idt,what="correlation created...")
    await asyncio.sleep(0)

    mds3 = sync_function(idt,mapper=False)
    await  send_message_to_socket(client_id=idt,what="main_data_structure 3 created...")
    await asyncio.sleep(0)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )