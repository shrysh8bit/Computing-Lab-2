run:
	(cat ../dataset/event1.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event2.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event3.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event4.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event5.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event6.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event7.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event8.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event9.txt | python3 mapper1.py | python3 combiner1.py \
	& cat ../dataset/event10.txt | python3 mapper1.py | python3 combiner1.py) \
	|python3 reducer1.py | sort -n | python3 mapper2.py | python3 reducer2.py | sort -n > result_event.txt
