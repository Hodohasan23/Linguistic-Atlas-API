import { useEffect, useRef } from "react";
import L from "leaflet";
import { mockLanguages, MACROAREA_COLORS } from "@/data/mock";
import "leaflet/dist/leaflet.css";

export default function MapPage() {
  const mapRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

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

    mockLanguages.forEach((lang) => {
      const color = MACROAREA_COLORS[lang.macroarea] || "#888";
      L.circleMarker([lang.latitude, lang.longitude], {
        radius: 7,
        color,
        fillColor: color,
        fillOpacity: 0.85,
        weight: 2,
      })
        .addTo(map)
        .bindPopup(
          `<div style="min-width:180px;padding:4px">
            <p style="font-weight:600;font-size:15px;margin:0">${lang.name}</p>
            <p style="color:#666;margin:4px 0 0">${lang.macroarea}</p>
            <p style="font-family:monospace;font-size:12px;color:#888;margin:8px 0 0">
              ${lang.latitude.toFixed(4)}, ${lang.longitude.toFixed(4)}
            </p>
          </div>`
        );
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  return (
    <div className="relative flex flex-col" style={{ height: "calc(100vh - 4rem)" }}>
      {/* Legend */}
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
