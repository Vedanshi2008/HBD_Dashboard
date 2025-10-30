import React, { useState, useEffect } from "react";
import {
  Card,
  CardHeader,
  Typography,
  Chip,
  CardBody,
} from "@material-tailwind/react";
import api from "../../utils/Api";

const BusinessCategory = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");

  const limit = 1000;
  const totalPages = Math.ceil(totalRecords / limit);

useEffect(() => {
  const delayDebounce = setTimeout(() => {
    if (search.trim() === "") {
      fetchData(currentPage);
    } else {
      fetchSearchResults(search);
    }
  }, 500); // wait for 500ms after user stops typing

  return () => clearTimeout(delayDebounce);
}, [search, currentPage]);


  const fetchData = async (page, searchTerm = "") => {
    setLoading(true);
    try {
      const response = await api.get(
        `/read_master_input/?page=${page}&limit=${limit}`
      );
      const result = await response.json();
      setData(result.data || []);
      setTotalRecords(result.total_records || 0);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

const fetchSearchResults = async (query) => {
  setLoading(true);
  try {
    const response = await api.get(`/search?query=${query}`);
    const result = await response.json();
    setData(result || []);
    setTotalRecords(result.total_records || 0); // fallback if no total_records
  } catch (error) {
    console.error("Error searching data:", error);
  } finally {
    setLoading(false);
  }
};
  
  return (
    <div className="mt-12 mb-8 flex flex-col gap-12 px-4">
      <div className="flex justify-between items-center mb-4">
        <Typography variant="h4" color="blue-gray">
          Business Category Data
        </Typography>
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => {
            setCurrentPage(1);
            setSearch(e.target.value);
          }}
          className="border rounded-lg px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <Card>
        <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
          <Typography variant="h6" color="white">
            Business Category
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          {loading ? (
            <p className="text-center text-blue-500 font-semibold">Loading...</p>
          ) : (
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["ID", "category","city","name","area","address","phone_no_1","phone_no_2","url","ratings","Sub Category","State","Country","Email","Latitude","Longitude"].map((head) => (
                    <th
                      key={head}
                      className="border-b border-blue-gray-50 py-3 px-5 text-left"
                    >
                      <Typography
                        variant="small"
                        className="text-[11px] font-bold uppercase text-blue-gray-400"
                      >
                        {head}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((item, idx) => {
                  const className = `py-3 px-5 ${
                    idx === data.length - 1 ? "" : "border-b border-blue-gray-50"
                  }`;

                  return (
                    <tr key={item.id}>
                      <td className={className}>{item.id}</td>
                      <td className={className}>{item.category}</td>
                      <td className={className}>{item.city}</td>
                      <td className={className}>{item.name}</td>
                      <td className={className}>{item.area}</td>
                      <td className={className}>{item.address}</td>
                      <td className={className}>{item.phone_no_1}</td>
                      <td className={className}>{item.phone_no_2}</td>
                      <td className={className}>{item.url}</td>
                      <td className={className}>{item.ratings}</td>
                      <td className={className}>{item.sub_category}</td>
                      <td className={className}>{item.state}</td>
                      <td className={className}>{item.country}</td>
                      <td className={className}>{item.email}</td>
                      <td className={className}>{item.latitude}</td>
                      <td className={className}>{item.longitude}</td>
                      {/* <td className={className}>
                        <Chip
                          variant="gradient"
                          color="green"
                          value="active"
                          className="py-0.5 px-2 text-[11px] font-medium w-fit"
                        />
                      </td> */}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>

      {/* Pagination */}
      <div className="flex justify-center items-center mt-6 gap-2 flex-wrap">
        <button
          className="px-3 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300"
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((p) => p - 1)}
        >
          Previous
        </button>
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index}
            onClick={() => setCurrentPage(index + 1)}
            className={`px-3 py-1 rounded border ${
              currentPage === index + 1
                ? "bg-blue-500 text-white"
                : "bg-white text-blue-500"
            }`}
          >
            {index + 1}
          </button>
        ))}
        <button
          className="px-3 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300"
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage((p) => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default BusinessCategory;
