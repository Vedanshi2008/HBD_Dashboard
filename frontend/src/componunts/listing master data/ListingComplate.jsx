import React, { useEffect, useState, useCallback } from "react";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Spinner,
  Chip,
} from "@material-tailwind/react";
import {
  ChevronUpDownIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
} from "@heroicons/react/24/solid";
import * as XLSX from "xlsx/dist/xlsx.full.min.js";
import api from "@/utils/Api"; // Ensure this points to your configured Axios instance

// 1. Updated Columns to match your 'ListingMaster' model
// Updated columns for Summary View
const completeColumns = [
  { key: "business_name", label: "Store / Business Name", width: 300 },
  { key: "category", label: "Service / Category", width: 200 },
  { key: "total_listings", label: "Total Listings", width: 150 },
  { key: "sources", label: "Found On Sources", width: 250 },
];
const ListingComplete = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [filteredData, setFilteredData] = useState([]); // For client-side filtering
  const [error, setError] = useState(null);

  // Search States
  const [search, setSearch] = useState("");
  const [categorySearch, setCategorySearch] = useState("");

  // 2. Fetch Function pointing to your new Python Route
  const fetchCompleteData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Calling the Flask Route: /api/listing-master
      const response = await api.get("/api/listing-master");

      // The API returns an array of objects directly
      const data = response.data || [];
      setPageData(data);
      setFilteredData(data); 

    } catch (err) {
      console.error("Fetch Error:", err);
      setError("Failed to fetch data from Master Table.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial Fetch
  useEffect(() => {
    fetchCompleteData();
  }, [fetchCompleteData]);

  // 3. Client-Side Filtering Logic (Since API sends all 100 records for now)
  useEffect(() => {
    let result = pageData;

    if (search) {
      result = result.filter(item => 
        item.business_name?.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (categorySearch) {
      result = result.filter(item => 
        item.category?.toLowerCase().includes(categorySearch.toLowerCase())
      );
    }

    setFilteredData(result);
  }, [search, categorySearch, pageData]);

  const exportToExcel = () => {
    if (!filteredData.length) return;
    const ws = XLSX.utils.json_to_sheet(filteredData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Complete_Listings");
    XLSX.writeFile(wb, `Listing_Master_Data.xlsx`);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-white text-black">
      <div className="flex justify-between items-end mb-6">
        <div>
          <Typography variant="h4" className="font-bold text-blue-gray-900">
            Listing Master Data
          </Typography>
          <Typography variant="small" className="font-medium text-gray-500">
            {error ? (
              <span className="text-red-500 font-bold">{error}</span>
            ) : (
              `Displaying verified complete records (${filteredData.length} total)`
            )}
          </Typography>
        </div>
        <div className="flex gap-2">
          <Button
            variant="gradient"
            color="green"
            size="sm"
            className="flex items-center gap-2"
            onClick={exportToExcel}
          >
            <ArrowDownTrayIcon className="h-4 w-4" /> Export
          </Button>
          <Button
            variant="outlined"
            size="sm"
            className="flex items-center gap-2"
            onClick={fetchCompleteData}
          >
            <ArrowPathIcon className="h-4 w-4" /> Refresh
          </Button>
        </div>
      </div>

      <Card className="h-full w-full border border-blue-gray-100">
        <CardHeader floated={false} shadow={false} className="rounded-none p-4 bg-blue-gray-50/50">
          <div className="flex flex-wrap items-center justify-between gap-y-4">
            <div className="flex w-full shrink-0 gap-2 md:w-max">
              <div className="w-72">
                <Input
                  label="Search Business Name"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              <div className="w-48">
                <Input
                  label="Filter by Category"
                  value={categorySearch}
                  onChange={(e) => setCategorySearch(e.target.value)}
                />
              </div>
            </div>
          </div>
        </CardHeader>

        <CardBody className="overflow-x-auto p-0">
          {loading ? (
            <div className="flex flex-col justify-center py-24 items-center gap-4">
              <Spinner className="h-10 w-10 text-blue-500" />
              <Typography className="animate-pulse font-medium text-gray-600">
                Loading Master Data...
              </Typography>
            </div>
          ) : (
            <table className="w-full min-w-[1200px] table-fixed text-left">
              <thead>
                <tr>
                  {completeColumns.map((col) => (
                    <th
                      key={col.key}
                      style={{ width: col.width }}
                      className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4"
                    >
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="flex items-center justify-between gap-2 font-bold leading-none opacity-70"
                      >
                        {col.label} <ChevronUpDownIcon strokeWidth={2} className="h-4 w-4" />
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
              {filteredData.length > 0 ? (
  filteredData.map((row, index) => (
    <tr key={index} className="even:bg-blue-gray-50/50 hover:bg-blue-50 transition-colors">
      {completeColumns.map((col) => (
        <td key={col.key} className="p-4 border-b border-blue-gray-50">
          {col.key === "sources" ? (
            <div className="flex flex-wrap gap-1">
              {/* Split the comma-separated sources and show badges */}
              {row[col.key]?.split(",").map((src, i) => (
                <Chip
                  key={i}
                  variant="ghost"
                  size="sm"
                  value={src}
                  color={
                    src === "JustDial" ? "orange" :
                    src === "GoogleMap" ? "green" :
                    src === "AskLaila" ? "red" : "blue"
                  }
                  className="rounded-full px-2 py-1 text-[10px]"
                />
              ))}
            </div>
          ) : col.key === "total_listings" ? (
             <div className="flex items-center gap-2">
                <span className="font-bold text-blue-gray-800 text-lg">
                    {row[col.key]}
                </span>
                <span className="text-xs text-gray-500">records</span>
             </div>
          ) : (
            <Typography variant="small" color="blue-gray" className="font-semibold">
              {row[col.key] || "-"}
            </Typography>
          )}
        </td>
      ))}
    </tr>
  ))
) : (
                  <tr>
                    <td colSpan={completeColumns.length} className="p-20 text-center">
                      <Typography variant="h6" color="blue-gray" className="opacity-40 italic">
                        {error || "No records found in Master Table"}
                      </Typography>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default ListingComplete;