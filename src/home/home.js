import React, { useState } from "react";
import ProductList from "./productlist";
import SearchBar from "./searchbar";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [showResults, setShowResults] = useState(false);

  const handleSearch = (term) => {
    setSearchTerm(term);
    setShowResults(true); // Trigger results view
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gradient-to-b from-white to-sky-300">
      {/* Heading and Slogan */}
      {!showResults && (
        <div className="text-center mb-4 mt-20">
          <h1 className="text-3xl font-bold text-gray-800">
            Find The Best Product With Our Recommendations
          </h1>
          <p className="mt-4 text-gray-600 text-2xl">Smart shopping made simple</p>
        </div>
      )}

      {/* Search Bar */}
      <div
        className={`w-full px-4 transition-all duration-500 mt-20 ${
          showResults ? "mt-4" : "mt-20"
        }`}
      >
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Product List */}
      {showResults && (
        <div className="w-full mt-6 px-4">
          <ProductList searchTerm={searchTerm} />
        </div>
      )}
    </div>
  );
};

export default Home;
