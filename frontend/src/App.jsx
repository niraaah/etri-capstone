import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Layout from "./Layout";
import ReportList from "./pages/ReportList";
import ReportDetail from "./pages/ReportDetail";
import SearchPapers from "./pages/SearchPapers";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/search" replace />} />
          <Route path="/reports" element={<ReportList />} />
          <Route path="/search" element={<SearchPapers />} />
          <Route path="/reports/:reportId" element={<ReportDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
