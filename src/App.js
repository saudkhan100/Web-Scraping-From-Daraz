import { Route, Routes } from "react-router-dom";
import Header from "./navigation-component/header";
import Home from "./home/home";

function App() {
  return (
    <div>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
