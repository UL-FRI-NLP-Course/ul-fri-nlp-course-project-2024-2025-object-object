SPARQL_MUNICIPALITIES_REGIONS = """
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

SPARQL_RIVERS_LENGTH = """
SELECT ?river ?riverLabel ?length ?mouth ?mouthLabel ?basinCountry ?basinCountryLabel ?tributary ?tributaryLabel
WHERE {
	# ?river is an instance (P31) of river (Q4022)
	?river wdt:P31 wd:Q4022.
	# ?river is located in the country (P17) Slovenia (Q215)
	?river wdt:P17 wd:Q215.
	# Optionally, get the length (P2043) of the river
	OPTIONAL { ?river wdt:P2043 ?length. }
	# Optional: Mouth of the watercourse (P403)
	OPTIONAL { ?river wdt:P403 ?mouth. }
	# Optional: Basin Country (P205) - can be multiple
	OPTIONAL { ?river wdt:P205 ?basinCountry. }
	# Optional: Tributary (P973) - can be multiple
	OPTIONAL { ?river wdt:P973 ?tributary. }


	# Get labels in Slovene (sl) - fallback to English (en)
	SERVICE wikibase:label { bd:serviceParam wikibase:language "sl,en". }
}
ORDER BY ?riverLabel
"""

SPARQL_PEAKS_ELEVATION = """
SELECT ?peak ?peakLabel ?elevation ?adminEntity ?adminEntityLabel
       ?prominence
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
LIMIT 20 # Get top 20 highest peaks
"""

SPARQL_CASTLES_LOCATION = """
SELECT ?castle ?castleLabel ?inception ?style ?styleLabel
       ?heritage ?heritageLabel ?adminEntity ?adminEntityLabel
WHERE {
	# ?castle is instance of castle (Q23413) or related types like fortress (Q57821)
	{ ?castle wdt:P31 wd:Q23413. } UNION { ?castle wdt:P31 wd:Q57821. }
	# Located in Slovenia (P17)
	?castle wdt:P17 wd:Q215.

	# Optional: Inception (P571)
	OPTIONAL { ?castle wdt:P571 ?inception. }
	# Optional: Architectural style (P149)
	OPTIONAL { ?castle wdt:P149 ?style. }
	# Optional: Heritage designation (P1435)
	OPTIONAL { ?castle wdt:P1435 ?heritage. }
	# Optional: Located in administrative entity (P131)
	OPTIONAL { ?castle wdt:P131 ?adminEntity. }

	SERVICE wikibase:label { bd:serviceParam wikibase:language "sl,en". }
}
ORDER BY ?castleLabel
LIMIT 100 # Limit results if there are many castles
"""