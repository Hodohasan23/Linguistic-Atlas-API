import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { mockLanguages, MACROAREA_COLORS } from "@/data/mock";
import { Globe, Users, MapPin } from "lucide-react";

const PIE_COLORS = ["#3b82c4", "#d9734c", "#5a9e6f", "#8b5ec4", "#d4953a", "#1ba8b0", "#e87ea1", "#6b8fbd"];

export default function AnalyticsPage() {
  const macroareaData = useMemo(() => {
    const counts: Record<string, number> = {};
    mockLanguages.forEach((l) => {
      counts[l.macroarea] = (counts[l.macroarea] || 0) + 1;
    });
    return Object.entries(counts).map(([name, count]) => ({
      name,
      count,
      fill: MACROAREA_COLORS[name] || "#888",
    }));
  }, []);

  const familyData = useMemo(() => {
    const counts: Record<string, number> = {};
    mockLanguages.forEach((l) => {
      counts[l.family] = (counts[l.family] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value);
  }, []);

  const stats = useMemo(() => {
    const families = new Set(mockLanguages.map((l) => l.family));
    const countries = new Set(mockLanguages.map((l) => l.country));
    return {
      total: mockLanguages.length,
      families: families.size,
      countries: countries.size,
    };
  }, []);

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6">
      <div>
        <h1 className="font-display text-3xl font-bold tracking-tight text-foreground">
          Analytics
        </h1>
        <p className="mt-1 text-muted-foreground">
          Overview of the linguistic database
        </p>
      </div>

      {/* Stat cards */}
      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard icon={Globe} label="Total Languages" value={stats.total} />
        <StatCard icon={Users} label="Language Families" value={stats.families} />
        <StatCard icon={MapPin} label="Countries" value={stats.countries} />
      </div>

      {/* Charts */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="rounded-2xl shadow-sm">
          <CardHeader>
            <CardTitle className="font-display text-lg">Languages by Macroarea</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={macroareaData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(214, 20%, 89%)" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {macroareaData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="rounded-2xl shadow-sm">
          <CardHeader>
            <CardTitle className="font-display text-lg">Languages by Family</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie
                  data={familyData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={110}
                  paddingAngle={2}
                  dataKey="value"
                  nameKey="name"
                  label={({ name }) => name}
                >
                  {familyData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: number;
}) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardContent className="flex items-center gap-4 p-6">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
          <Icon className="h-6 w-6 text-primary" />
        </div>
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="font-display text-2xl font-bold text-foreground">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
}
