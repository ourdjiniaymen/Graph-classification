import React from "react";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import Kernel from "./Kernel";
import DataSet from "./DataSet";
import Result from "./Result";
import Classification from "./Classification";

const TabsContainer = () => {
  const [value, setValue] = React.useState("1");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

  return (
    <div style={{ height: 400, width: "90%", margin: "auto", padding: "10px" }}>
      <Box sx={{ width: "100%", typography: "body1" }}>
        <TabContext value={value}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <TabList
              onChange={handleChange}
              aria-label="lab API tabs example"
              variant="fullWidth"
            >
              <Tab label="Kernels" value="1" />
              <Tab label="Data sets" value="2" />
              <Tab label="Results" value="3" />
              <Tab label="Classification" value="4" />
            </TabList>
          </Box>
          <TabPanel value="1">
            <Kernel />
          </TabPanel>
          <TabPanel value="2">
            <DataSet />
          </TabPanel>
          <TabPanel value="3">
            <Result />
          </TabPanel>
          <TabPanel value="4">
            <Classification />
          </TabPanel>
        </TabContext>
      </Box>
    </div>
  );
};

export default TabsContainer;
