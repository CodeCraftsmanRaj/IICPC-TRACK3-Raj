import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldCheck } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  // Automatically redirect to the dashboard
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 2000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 mb-6">
        <ShieldCheck className="h-8 w-8 text-primary" />
      </div>
      <h1 className="mb-2 text-3xl font-bold tracking-tight text-foreground">ProctorGuard System</h1>
      <p className="text-muted-foreground mb-8">VM & Remote Access Detection Engine</p>
      
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <div className="h-2 w-2 animate-pulse rounded-full bg-primary"></div>
        <span>Loading Dashboard...</span>
      </div>
    </div>
  );
};

export default Index;