import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Result from "../../../business/domain/Result";
import Table from "./Table";
import { GridColDef } from "@mui/x-data-grid";

const resultColumns: GridColDef[] = [
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

interface Props {
  open: boolean;
  handleClose: () => void;
  result: Result;
}

const ResultDialog = ({ open, handleClose, result }: Props) => {
  const test = {
    id: 0,
    kernel: result.kernel,
    dataset: result.dataset,
    accuracy: result.accuracy,
    standard_deviation: result.standard_deviation,
    running_time: result.running_time,
    rbf: result.rbf,
    sigma: result.sigma,
    normalize: result.normalize,
    c: result.c,
    cv: result.cv,
    experiments: result.experiments,
    with_labels: result.with_labels,
    with_attributes: result.with_attributes,
    parameters: result.parameters,
  }; 
  return (
    <React.Fragment>
      <Dialog
        fullWidth={true}
        maxWidth={"lg"}
        open={open}
        onClose={handleClose}
      >
        <DialogTitle>Result</DialogTitle>
        <DialogContent>
          <DialogContentText></DialogContentText>
          <Table
            columns={resultColumns}
            rows={[test]}
            height={200}
            padding={"0px"}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

export default ResultDialog;
