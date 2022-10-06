import React from "react";

const Header = () => {
  return (
    <>
      <nav className="navbar navbar-dark bg-primary">
        <div>
          <img
            className="mb-3 ms-3"
            src="http://localhost:9000/logo.png"
            height={35}
            width={35}
          />
          <span className="navbar-brand ms-1 h1">Graph Kernels</span>
        </div>
      </nav>
    </>
  );
};

export default Header;