import React, { useEffect } from "react";
import { GridColDef } from "@mui/x-data-grid";
import CircularProgressPage from "./CircularProgressPage";
import Table from "./Table";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { GetResultsEvents } from "../viewmodel/events/GetResultsEvents";

const resultColumns: GridColDef[] = [
  {
    field: "id",
    headerName: "#",
    width: 70,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "kernel",
    headerName: "Kernel",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "dataset",
    headerName: "Data set",
    align: "center",
    headerAlign: "center",
  },
  {
    field: "accuracy",
    headerName: "Accuracy",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "standard_deviation",
    headerName: "Standard deviation",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "running_time",
    headerName: "Running time",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "rbf",
    headerName: "Rbf",
    align: "center",
    type: "boolean",
    headerAlign: "center",
  },
  {
    field: "sigma",
    headerName: "Sigma",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "normalize",
    headerName: "Normalize",
    align: "center",
    type: "boolean",
    headerAlign: "center",
  },
  {
    field: "c",
    headerName: "C",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "cv",
    headerName: "Cv",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "experiments",
    headerName: "Experiments",
    align: "center",
    type: "number",
    headerAlign: "center",
  },
  {
    field: "with_labels",
    headerName: "With labels",
    align: "center",
    type: "boolean",
    headerAlign: "center",
  },
  {
    field: "with_attributes",
    headerName: "With attributes",
    align: "center",
    type: "boolean",
    headerAlign: "center",
  },
  {
    field: "parameters",
    headerName: "Parameters",
    align: "center",
    headerAlign: "center",
  },
];

const Result = () => {
  const { isLoadingResult, results } = useAppSelector(
    (state) => state.ResultlSlice
  );
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(GetResultsEvents().getResultsEvent());
  }, [dispatch]);

  return (
    <div>
      {isLoadingResult ? (
        <CircularProgressPage isLoading={isLoadingResult} />
      ) : (
        <Table columns={resultColumns} rows={results} />
      )}
    </div>
  );
};

export default Result;
