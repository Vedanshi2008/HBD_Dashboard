import { Button, Card, CardBody, CardHeader, Typography } from '@material-tailwind/react';
import React, { useEffect, useState } from 'react'
import api from '../../utils/Api';

const ProductComplate = () => {
   const [loading, setLoading] = useState(false);
   const [data , setData] = useState([])
   const [currentPage , setCurrentPage] = useState(1)
   const [totalRecords , setTotalRecords] = useState(0)
  
   const limit = 1000; 
   const totalPages = Math.ceil(totalRecords / limit);

     const fetchData = async () => {
      setLoading(true);
      try {
        const response = await api.get(`/products/complete`);
       
        setData(response.data.data || []);
        setTotalRecords(response.data.count || 0);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    useEffect(() => {
      fetchData();
    },[])
  return (
    <div className="mt-12 mb-8 flex flex-col gap-12 px-4">
      {/* <div className="flex justify-between items-center mb-4">
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
      </div> */}

      <Card>
        <CardHeader
          variant="gradient"
          color="gray"
          className="mb-8 p-4 flex items-center justify-between"
        >
          {/* Left: Title */}
          <Typography variant="h6" color="white">
           Product Complate Data
          </Typography>

          {/* Right: Button + Total */}
          <div className="flex items-center gap-4">
            <Button
              variant="outlined"
              color="white"
              className="flex items-center gap-2"
              // onClick={() => downloadCSV("complete")}
              onClick={() => console.log("Download CSV")}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
                />
              </svg>
              Download Csv
            </Button>

            <Typography variant="h6" color="white">
              Total: {totalRecords}
            </Typography>
          </div>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          {loading ? (
            <p className="text-center text-blue-500 font-semibold">Loading...</p>
          ) : (
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["ID","ASIN", "Product_name","price","rating","Number_of_ratings","Brand","Seller","category","subcategory","sub_sub_category","category_sub_sub_sub","colour","size_options","description","link","Image_URLs","About_the_items_bullet","Product_details","Additional_Details","Manufacturer_Name","created_at"].map((head) => (
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
                      <td className={className}>{item.ASIN}</td>
                      <td className={className}>{item.Product_name}</td>
                      <td className={className}>{item.price}</td>
                      <td className={className}>{item.rating}</td>
                      <td className={className}>{item.Number_of_ratings}</td>
                      <td className={className}>{item.Brand}</td>
                      <td className={className}>{item.Seller}</td>
                      <td className={className}>{item.category}</td>
                      <td className={className}>{item.subcategory}</td>
                      <td className={className}>{item.sub_sub_category}</td>
                      <td className={className}>{item.category_sub_sub_sub}</td>
                      <td className={className}>{item.colour}</td>
                      <td className={className}>{item.size_options}</td>
                      <td className={className}>{item.description}</td>
                      <td className={className}>{item.link}</td>
                      <td className={className}>{item.Image_URLs}</td> 
                      <td className={className}>{item.About_the_items_bullet}</td> 
                      <td className={className}>{item.Manufacturer_Name}</td> 
                      <td className={className}>{item.Manufacturer_Name}</td> 
                      <td className={className}>{item.Manufacturer_Name}</td> 
                      <td className={className}>{item.created_at}</td> 
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
  )
}

export default ProductComplate