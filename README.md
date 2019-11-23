# IAP
Interaction analysis program

This program collects data from 9gag and analyse the interactivity of the users.



To run the script, simply do
```
python3 main.py
```

The script will output a json file that contains the data it collected. The data is constructed from 60 featured posts on 9gag.

If you want to have a more simpilified csv version of the data, you can do:

```
python3 json2csv.py
```

The program will prompt you to enter the path of the json file generated by the main script.