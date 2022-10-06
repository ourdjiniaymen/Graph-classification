import React, { useEffect } from "react";
import { GridColDef } from "@mui/x-data-grid";
import CircularProgressPage from "./CircularProgressPage";
import Table from "./Table";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { GetKernelsEvents } from "../viewmodel/events/GetKernelsEvents";

const kernelColumns: GridColDef[] = [
  {
    field: "id",
    headerName: "#",
    width: 70,
    type: "number",
    align: "center",
    headerAlign: "center",
  },
  { field: "name", headerName: "Name", align: "center", headerAlign: "center", flex:1 },
  {
    field: "use_node_labels",
    headerName: "Use node labels",
    sortable: false,
    type: "boolean",
    align: "center",
    headerAlign: "center",
    flex:1,
  },
  {
    field: "use_node_attributes",
    headerName: "Use node attributes",
    sortable: false,
    type: "boolean",
    align: "center",
    headerAlign: "center",
    flex:1,
  },
  {
    field: "parameters",
    flex:1,
    headerName: "Parameters",
    sortable: false,
    align: "center",
    headerAlign: "center",
  },
];

const Kernel = () => {
  const { isLoadingKernel, kernels } = useAppSelector(
    (state) => state.KernelSlice
  );
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(GetKernelsEvents().getKernelsEvent());
  }, [dispatch]);

  return (
    <div>
      {isLoadingKernel ? (
        <CircularProgressPage isLoading={isLoadingKernel} />
      ) : (
        <Table columns={kernelColumns} rows={kernels} />
      )}
    </div>
  );
};

export default Kernel;
