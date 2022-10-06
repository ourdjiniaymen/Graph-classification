import React, { useEffect } from "react";
import { GridColDef } from "@mui/x-data-grid";
import CircularProgressPage from "./CircularProgressPage";
import Table from "./Table";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { GetDataSetsEvents } from "../viewmodel/events/GetDataSetsEvents";

const dataSetColumns: GridColDef[] = [
  {
    field: "id",
    headerName: "#",
    width: 70,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "name",
    headerName: "Name",
    flex: 1,
    align: "center",
    headerAlign: "center",
  },
  {
    field: "number_graphs",
    headerName: "Number graphs",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "number_classes",
    headerName: "Number classes",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "classes_imbalance",
    headerName: "Classes imbalance",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "average_nodes",
    headerName: "Average nodes",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "average_edges",
    headerName: "Average edges",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "labels_number",
    headerName: "Labels number",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "attribute_dimension",
    headerName: "Attribute dimension",
    flex: 1,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
];

const DataSet = () => {
  const { isLoadingDataSet, dataSets } = useAppSelector(
    (state) => state.DataSetSlice
  );
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(GetDataSetsEvents().getDataSetsEvent());
  }, [dispatch]);

  return (
    <div>
      {isLoadingDataSet ? (
        <CircularProgressPage isLoading={isLoadingDataSet} />
      ) : (
        <Table columns={dataSetColumns} rows={dataSets} />
      )}
    </div>
  );
};

export default DataSet;
