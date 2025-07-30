// import React, { useEffect, useState } from "react";

// const ProductList = ({ searchTerm }) => {
//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sortOption, setSortOption] = useState("none");
//   const [filterOption, setFilterOption] = useState("all");

//   useEffect(() => {
//     const fetchProducts = async () => {
//       if (!searchTerm) return;

//       setLoading(true);
//       setError(null);

//       try {
//         const response = await fetch(`http://localhost:8000/api/search?query=${searchTerm}`);

//         if (!response.ok) {
//           throw new Error("Failed to fetch products.");
//         }

//         const result = await response.json();
//         console.log(result.data);

//         if (result.success) {
//           setProducts(result.data);
//         } else {
//           throw new Error(result.message || "Failed to fetch products.");
//         }
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchProducts();

//     return () => setLoading(false);
//   }, [searchTerm]);

//   const handleSort = (option) => {
//     setSortOption(option);
//   };

//   const handleFilter = (option) => {
//     setFilterOption(option);
//   };

//   const sortedProducts = (() => {
//     let filteredProducts = [...products];

//     // Apply filtering based on ratings
//     if (filterOption === "high") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 4);
//     } else if (filterOption === "normal") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 3 && product.stars < 4);
//     } else if (filterOption === "low") {
//       filteredProducts = filteredProducts.filter((product) => product.stars >= 1 && product.stars < 3);
//     }

//     // Apply sorting
//     if (sortOption === "price-asc") {
//       return filteredProducts.sort((a, b) => a.price - b.price);
//     } else if (sortOption === "price-desc") {
//       return filteredProducts.sort((a, b) => b.price - a.price);
//     }

//     return filteredProducts;
//   })();

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
//       </div>
//     );
//   }

//   if (error) {
//     return <div className="text-center text-red-500">Error: {error}</div>;
//   }

//   if (!products.length) {
//     return <div className="text-center text-lg">No products found.</div>;
//   }

//   return (
//     <div className="flex justify-center">
//       <div className="w-11/12">
//         {/* Sorting and Filtering Controls */}
//         <div className="mb-4 flex justify-between">
//           {/* Sort Dropdown */}
//           <select
//             value={sortOption}
//             onChange={(e) => handleSort(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="none">No Sorting</option>
//             <option value="price-asc">Price: Low to High</option>
//             <option value="price-desc">Price: High to Low</option>
//           </select>

//           {/* Filter Dropdown */}
//           <select
//             value={filterOption}
//             onChange={(e) => handleFilter(e.target.value)}
//             className="border p-2 rounded-md"
//           >
//             <option value="all">All Ratings</option>
//             <option value="high">High Ratings (4-5)</option>
//             <option value="normal">Normal Ratings (3-4)</option>
//             <option value="low">Low Ratings (1-3)</option>
//           </select>
//         </div>

//         {/* Product Grid */}
//         <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//           {sortedProducts.map((product, index) => (
//             <a
//               target="_blank"
//               rel="noopener noreferrer"
//               href={product.link}
//               key={index}
//               className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
//             >
//               {/* Product Image */}
//               <img
//                 src={product.image_url}
//                 alt={product.title}
//                 className="w-full h-40 object-contain mb-4"
//               />

//               {/* Product Title */}
//               <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
//                 {product.title}
//               </h2>

//               {/* Product Price */}
//               <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

//               {/* Rating & Stars */}
//               <div className="flex items-center justify-between w-full text-sm">
//                 <div className="flex items-center">
//                   <span className="mr-1">★</span>
//                   <span className="font-semibold">{product.stars || "N/A"}</span>
//                   <span>/5</span>
//                 </div>
//                 <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
//                   {product.score || "0"}/10
//                 </div>
               
//               </div>

//               {product.user_reviews && product.user_reviews.length > 0 && (
//                 <div className="mt-4 w-full">
//                   <h3 className="text-sm font-semibold mb-2">User Reviews:</h3>
//                   <ul>
//                     {product.user_reviews.map((review, index) => (
//                       <li key={index} className="text-xs text-gray-600 mb-2">
//                         {review}
//                       </li>
//                     ))}
//                   </ul>
//                 </div>
//               )}
//             </a>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProductList;


import React, { useEffect, useState } from "react";

const ProductList = ({ searchTerm }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sortOption, setSortOption] = useState("none");
  const [filterOption, setFilterOption] = useState("all");

  useEffect(() => {
    const fetchProducts = async () => {
      if (!searchTerm) return;

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`http://localhost:8000/api/search?query=${searchTerm}`);

        if (!response.ok) {
          throw new Error("Failed to fetch products.");
        }

        const result = await response.json();
        console.log(result.data);

        if (result.success) {
          setProducts(result.data);
        } else {
          throw new Error(result.message || "Failed to fetch products.");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();

    return () => setLoading(false);
  }, [searchTerm]);

  const handleSort = (option) => {
    setSortOption(option);
  };

  const handleFilter = (option) => {
    setFilterOption(option);
  };

  const sortedProducts = (() => {
    let filteredProducts = [...products];

    // Apply filtering based on ratings
    if (filterOption === "high") {
      filteredProducts = filteredProducts.filter((product) => product.stars >= 4);
    } else if (filterOption === "normal") {
      filteredProducts = filteredProducts.filter((product) => product.stars >= 3 && product.stars < 4);
    } else if (filterOption === "low") {
      filteredProducts = filteredProducts.filter((product) => product.stars >= 1 && product.stars < 3);
    }

    // Apply sorting
    if (sortOption === "price-asc") {
      return filteredProducts.sort((a, b) => a.price - b.price);
    } else if (sortOption === "price-desc") {
      return filteredProducts.sort((a, b) => b.price - a.price);
    }

    return filteredProducts;
  })();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-red-500">Error: {error}</div>;
  }

  if (!products.length) {
    return <div className="text-center text-lg">No products found.</div>;
  }

  return (
    <div className="flex justify-center">
      <div className="w-11/12">
        {/* Sorting and Filtering Controls */}
        <div className="mb-4 flex justify-between">
          {/* Sort Dropdown */}
          <select
            value={sortOption}
            onChange={(e) => handleSort(e.target.value)}
            className="border p-2 rounded-md"
          >
            <option value="none">No Sorting</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
          </select>

          {/* Filter Dropdown */}
          <select
            value={filterOption}
            onChange={(e) => handleFilter(e.target.value)}
            className="border p-2 rounded-md"
          >
            <option value="all">All Ratings</option>
            <option value="high">High Ratings (4-5)</option>
            <option value="normal">Normal Ratings (3-4)</option>
            <option value="low">Low Ratings (1-3)</option>
          </select>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
          {sortedProducts.map((product, index) => (
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={product.link}
              key={index}
              className="border rounded-lg p-4 flex flex-col items-center bg-white shadow-lg hover:shadow-xl transition"
            >
              {/* Product Image */}
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-40 object-contain mb-4"
              />

              {/* Product Title */}
              <h2 className="text-md mb-2 text-left w-full whitespace-nowrap overflow-hidden text-ellipsis">
                {product.title}
              </h2>

              {/* Product Price */}
              <p className="text-gray-700 font-bold mb-2">Rs {product.price}</p>

              {/* Rating & Stars */}
              <div className="flex items-center justify-between w-full text-sm">
                <div className="flex items-center">
                  <span className="mr-1">★</span>
                  <span className="font-semibold">{product.stars || "N/A"}</span>
                  <span>/5</span>
                </div>
                <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
                  {product.sentiment_score || "0"}/5
                </div>
              </div>

              {/* User Reviews */}
              {product.user_reviews && product.user_reviews.length > 0 && (
                <div className="mt-4 w-full">
                  <h3 className="text-sm font-semibold mb-2">User Reviews:</h3>
                  <ul>
                    {product.user_reviews.map((reviewObj, index) => (
                      <li key={index} className="text-xs text-gray-600 mb-2">
                        <p>{reviewObj.review}</p>
                        <p className="text-xs text-gray-400">Sentiment Score: {reviewObj.sentiment_score}/5</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductList;
