SPARQL_MUNICIPALITIES = """
SELECT DISTINCT ?municipality ?municipalityLabel ?region ?regionLabel
				?population ?area ?inception ?mayor ?mayorLabel
WHERE {
	# ?municipality is an instance (P31) of municipality of Slovenia (Q328584)
	?municipality wdt:P31 wd:Q328584.

	# ?municipality located in statistical territorial entity (P8138) ?region.
	?municipality wdt:P8138 ?region.

	# Optional properties
	OPTIONAL { ?municipality wdt:P1082 ?population. } # Population
	OPTIONAL { ?municipality wdt:P2046 ?area. }       # Area

	# Get labels in Slovene (sl) - fallback to English (en)
	SERVICE wikibase:label { bd:serviceParam wikibase:language "sl,en". }
}
ORDER BY ?municipalityLabel
"""

SPARQL_PEAKS = """
SELECT ?peak ?peakLabel ?elevation ?adminEntity ?adminEntityLabel ?prominence
WHERE {
	# ?peak is an instance (P31) of peak (Q8502) or natural peak (Q207326)
	{ ?peak wdt:P31 wd:Q8502. } UNION { ?peak wdt:P31 wd:Q207326. }
	# ?peak is located in the country (P17) Slovenia (Q215)
	?peak wdt:P17 wd:Q215.
	# Get the elevation (P2044)
	?peak wdt:P2044 ?elevation.

	# Optional: Located in administrative entity (P131)
	OPTIONAL { ?peak wdt:P131 ?adminEntity. }
	# Optional: Prominence (P2656)
	OPTIONAL { ?peak wdt:P2656 ?prominence. }

	# Get labels in Slovene (sl) - fallback to English (en)
	SERVICE wikibase:label { bd:serviceParam wikibase:language "sl,en". }
}
ORDER BY DESC(?elevation) # Order by highest first
"""

SPARQL_CASTLES = """
SELECT ?castle ?castleLabel ?heritage ?heritageLabel ?adminEntity ?adminEntityLabel
WHERE {
	# ?castle is instance of castle (Q23413) or related types like fortress (Q57821)
	{ ?castle wdt:P31 wd:Q23413. } UNION { ?castle wdt:P31 wd:Q57821. }
	# Located in Slovenia (P17)
	?castle wdt:P17 wd:Q215.

	# Optional: Heritage designation (P1435)
	OPTIONAL { ?castle wdt:P1435 ?heritage. }
	# Optional: Located in administrative entity (P131)
	OPTIONAL { ?castle wdt:P131 ?adminEntity. }

	SERVICE wikibase:label { bd:serviceParam wikibase:language "sl,en". }
}
ORDER BY ?castleLabel
"""