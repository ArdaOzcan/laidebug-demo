cd laidebug_engine\laidebug_engine
python -m venv .
call .\Scripts\activate
pip install -r requirements.txt
deactivate

cd ..\..\laidebug_api
python -m venv .
call .\Scripts\activate
pip install -r requirements.txt
deactivate

