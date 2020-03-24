[![Build status](https://ci.appveyor.com/api/projects/status/fcpx00kw7gg5d5u5?svg=true)](https://ci.appveyor.com/project/jpmondet/ssapi)

# Playing with the ssapi


* [Averages by countries of Top N (for countries appearing in the global top M)](#averages-by-countries-of-top-n-for-countries-appearing-in-the-global-top-m)
   * [Requirements](#requirements)
   * [Simple usage](#simple-usage)
   * [Lil' more advanced usage](#lil-more-advanced-usage)
      * [Updating and/or getting more datas](#updating-andor-getting-more-datas)
      * [Modifying the default top15/top100](#modifying-the-default-top15top100)
      * [More flags](#more-flags)


## Averages by countries of Top N (for countries appearing in the global top M)

### Requirements

There is no dependency except using python 3 (python2 support should be easy to add but since it's deprecated...).

### Simple usage

`python top_n_average_by_county_from_top_n_global.py`

By default, this will scrap the first 200 pages and calculate the average of top 15 for countries appearing in the global top 100.  
The first time you launch it, it will also store the data of those 200 pages in a file so it won't have to scrap the API next time : 

```
PP average of the top15 players from all the countries appearing in the top100
US   10461.14
CA   9318.63
GB   9199.04
JP   8713.14
NL   8705.93
AU   8696.81
DE   8678.72
KR   8508.79
SE   8281.00
NO   8109.20
FR   8060.47
DK   7709.43
FI   7662.24
CN   7570.98
BE   7547.80
PL   7496.16
RU   7032.88
CZ   6947.99
CH   6880.24
AT   6841.45
ES   6356.52
IL   5829.07
SG   5515.96
```

### Lil' more advanced usage

#### Updating and/or getting more datas

If you want to scrap more pages (or to update the data stored in a local file), you have to use the `-u` flag with the number of pages you want, for example : 

`python top_n_average_by_county_from_top_n_global.py -u 100`

(**The API doesn't like that we scrap too much pages at once. Thus, a limit to 200 pages is applied for now.  
 A future patch will poll the API by chunks to avoid this behavior and allow for any number of pages**)

#### Modifying the default top15/top100

If you wanna get the averages of top 50 by countries for countries appearing in the top 200, just use the `-N` and `-M` flags, for example : 

`python top_n_average_by_county_from_top_n_global.py -N 50 -M 200`

#### More flags

You can use the help flag (`-h`) to get all the flags available : 

`python top_n_average_by_county_from_top_n_global.py -h`

```
usage: top_n [-h] [-N TOPN] [-M TOPM] [-u UPDATE] [-f FILESTORAGE]

Leverage ScoreSaber API to calculte the PP average of the top N players of
each countries appearing in the global top M players

optional arguments:
  -h, --help            show this help message and exit
  -N TOPN, --topN TOPN  Will calculate the average of the N players being at
                        the top of their country (15 by default)
  -M TOPM, --topM TOPM  Will check the countries appearing in the global top M
                        players to do its calculation (100 by default)
  -u UPDATE, --update UPDATE
                        If this flag is passed with a number > 0, the script
                        will poll the ScoreSaber API to get the number of
                        pages specified before calculation (MAY BE LONG) (by
                        default, the flag is set to 0 which means that it
                        won't poll the API and try to use the default stored
                        file. If there is no stored file, it will poll the
                        first 200 pages)
  -f FILESTORAGE, --filestorage FILESTORAGE
                        Specifies the file countaining already retrieved datas
                        from the API (polling the API being long, we avoid
                        doing it every time). (by default, the stored file is
                        'ssaber_pages_data.json')
```



