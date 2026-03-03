import { apiFetch } from "@/api/config";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useRef, useState } from "react";

type MapLanguage = {
  ID: string;
  Name: string;
  Macroarea: string | null;
  Latitude: number;
  Longitude: number;
  Level: string | null;
  ISO639P3code: string | null;
};

const MACROAREA_COLORS: Record<string, string> = {
  Africa: "#C96B4B",
  Eurasia: "#7A8F6A",
  Papunesia: "#8E6BBE",
  "North America": "#4C9BE8",
  "South America": "#2A9D8F",
  Australia: "#E9A03B",
};

export default function MapPage() {
  const mapRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);

  const [languages, setLanguages] = useState<MapLanguage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadMapData() {
      try {
        setLoading(true);
        setError(null);
        const data = await apiFetch<MapLanguage[]>("/languages/map?limit=500");
        setLanguages(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load map data");
      } finally {
        setLoading(false);
      }
    }

    loadMapData();
  }, []);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      center: [20, 0],
      zoom: 2,
      minZoom: 2,
      maxZoom: 12,
      scrollWheelZoom: true,
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
    }).addTo(map);

    markersLayerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
      markersLayerRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!markersLayerRef.current) return;

    markersLayerRef.current.clearLayers();

    languages.forEach((lang) => {
      if (lang.Latitude == null || lang.Longitude == null) return;

      const color = MACROAREA_COLORS[lang.Macroarea ?? ""] || "#888";

      L.circleMarker([lang.Latitude, lang.Longitude], {
        radius: 7,
        color,
        fillColor: color,
        fillOpacity: 0.85,
        weight: 2,
      })
        .addTo(markersLayerRef.current!)
        .bindPopup(
          `<div style="min-width:180px;padding:4px">
            <p style="font-weight:600;font-size:15px;margin:0">${lang.Name}</p>
            <p style="color:#666;margin:4px 0 0">${lang.Macroarea ?? "Unknown"}</p>
            <p style="margin:6px 0 0;font-size:12px;color:#666">${lang.Level ?? "—"}</p>
            <p style="margin:4px 0 0;font-size:12px;color:#666">ISO: ${lang.ISO639P3code ?? "—"}</p>
            <p style="font-family:monospace;font-size:12px;color:#888;margin:8px 0 0">
              ${lang.Latitude.toFixed(4)}, ${lang.Longitude.toFixed(4)}
            </p>
          </div>`
        );
    });
  }, [languages]);

  return (
    <div className="relative flex flex-col" style={{ height: "calc(100vh - 4rem)" }}>
      <div className="absolute left-4 top-4 z-[1000] rounded-xl border bg-card/90 px-4 py-3 shadow-lg backdrop-blur-sm">
        {loading && <p className="text-sm text-muted-foreground">Loading map data...</p>}
        {error && <p className="text-sm text-destructive">{error}</p>}
        {!loading && !error && (
          <p className="text-sm text-muted-foreground">
            Showing {languages.length} mapped languages
          </p>
        )}
      </div>

      <div className="absolute right-4 top-4 z-[1000] rounded-xl border bg-card/90 p-4 shadow-lg backdrop-blur-sm">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Macroareas
        </p>
        <div className="space-y-1.5">
          {Object.entries(MACROAREA_COLORS).map(([name, color]) => (
            <div key={name} className="flex items-center gap-2">
              <span
                className="inline-block h-3 w-3 rounded-full"
                style={{ backgroundColor: color }}
              />
              <span className="text-xs text-foreground">{name}</span>
            </div>
          ))}
        </div>
      </div>

      <div
        ref={containerRef}
        className="h-full w-full flex-1"
        style={{ background: "hsl(210, 20%, 95%)" }}
      />
    </div>
  );
}
