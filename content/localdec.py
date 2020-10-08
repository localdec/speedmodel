def mark_excursion(tool, speed_thresh, dist_thresh, pl):
    hssegs = pl[(pl["Velocity"] >= speed_thresh) & (pl["Tool"] == tool)]
    if hssegs.index.size != 0:
        pdist = hssegs.loc[hssegs.first_valid_index(),"Distance"] # starting distance
        peak = {
            "segid": None,
            "velocity": 0,
            "start": pdist,
            "end": None
        } # initialize peak holder
        for segid in hssegs.index:
            if hssegs.loc[segid, "Distance"] > (pdist + dist_thresh):
                # write new peak
                pl.loc[peak["segid"], "Excursion"] = 1
                pl.loc[peak["segid"], "Length"] = peak["end"] - peak["start"]
                peak["segid"] = segid
                peak["velocity"] =  hssegs.loc[segid, "Velocity"]
                peak["start"] =  hssegs.loc[segid, "Distance"]
            else:
                if (hssegs.loc[segid, "Velocity"] > peak["velocity"]):
                    peak["segid"] = segid
                    peak["velocity"] = hssegs.loc[segid, "Velocity"]
            pdist = hssegs.loc[segid, "Distance"]
            peak["end"] =  pdist
        # write final peak
        pl.loc[peak["segid"], "Excursion"] = 1
        pl.loc[peak["segid"], "Length"] = peak["end"] - peak["start"]
    return

