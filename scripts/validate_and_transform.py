
import json, sys, pathlib, csv, hashlib
from datetime import datetime
from jsonschema import validate, Draft202012Validator
from glob import glob

SCHEMA = json.load(open("schemas/resonance-reading.schema.json"))

def city_hash(city_like: str) -> str:
    return hashlib.sha256(city_like.encode()).hexdigest()[:12]

def shift_decimal(raw):
    return float(raw) / 10.0

def process_file(fp):
    data = json.load(open(fp))
    if "resonance_reading_hz_raw" in data and "resonance_reading_hz" not in data:
        data["resonance_reading_hz"] = shift_decimal(data["resonance_reading_hz_raw"])
    for k in ["name","email","phone","address"]:
        if k in data: data.pop(k)
    lb = data.get("location_band", {"level":"none"})
    if lb.get("level") == "coarse-city" and "city_hash" not in lb:
        if "city" in lb:
            lb["city_hash"] = city_hash(lb.pop("city"))
        else:
            lb["city_hash"] = None
    data["location_band"] = lb
    Draft202012Validator(SCHEMA).validate(data)
    return data

def write_csv(rows, out_csv):
    fields = ["timestamp","node_id","ufr_hz","delta_q","coherence",
              "resonance_reading_hz","hr_bpm","hrv_ms","stress_0_10",
              "location_band.level","location_band.city_hash","location_band.region",
              "solar_inputs.flare_class","solar_inputs.cme_count","solar_inputs.solar_wind_kmps",
              "solar_inputs.pressure_npa","solar_inputs.proton_density_pcc"]
    with open(out_csv,"w",newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for d in rows:
            lb = d.get("location_band",{})
            si = d.get("solar_inputs",{})
            w.writerow([
                d.get("timestamp"), d.get("node_id"), d.get("ufr_hz"),
                d.get("delta_q"), d.get("coherence"),
                d.get("resonance_reading_hz"),
                d.get("hr_bpm"), d.get("hrv_ms"), d.get("stress_0_10"),
                lb.get("level"), lb.get("city_hash"), lb.get("region"),
                si.get("flare_class"), si.get("cme_count"), si.get("solar_wind_kmps"),
                si.get("pressure_npa"), si.get("proton_density_pcc")
            ])

def main():
    inputs = sorted(glob("data/**/*.json", recursive=True))
    processed = []
    out_dir = pathlib.Path("processed")
    out_dir.mkdir(exist_ok=True)
    for fp in inputs:
        try:
            d = process_file(fp)
            processed.append(d)
            rel = pathlib.Path(fp).name
            json.dump(d, open(out_dir / rel, "w"), indent=2)
        except Exception as e:
            print(f"::error file={fp}::{e}")
            sys.exit(1)
    if processed:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        write_csv(processed, out_dir / f"{today}.csv")

if __name__ == "__main__":
    main()
