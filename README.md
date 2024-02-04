# TrainStreamer

0. Clone project and cd into its folder
1. Run main.py with
```
uvicorn backend.app.main:app --reload --host 0.0.0.0
```
2. Open http://localhost:8000/ in your browser
3. To try out the visualizations run the client example file with `python -m backend.client_example` to send a UDP message to the server containing random data
