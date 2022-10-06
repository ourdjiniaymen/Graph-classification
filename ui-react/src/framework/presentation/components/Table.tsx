import React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { padding } from "@mui/system";

interface Props {
  columns: GridColDef[];
  rows: any[];
  height?: number;
  padding?: string;
}

const Table = ({ columns, rows, height, padding }: Props) => {
  return (
    <>
      <div
        style={{
          height: height != null ? height : 400,
          width: "100%",
          margin: "auto",
          padding: padding != null ? padding : "10px",
        }}
      >
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection={false}
          autoHeight={true}
          headerHeight={80}
          disableColumnMenu={true}
          sx={{
            "& .MuiDataGrid-columnHeaderTitle": {
              textOverflow: "clip",
              whiteSpace: "break-spaces",
              lineHeight: 1,
            },
            "& .MuiDataGrid-cellContent": {
              textOverflow: "clip",
              whiteSpace: "break-spaces",
              lineHeight: 1,
            },
          }}
        />
      </div>
    </>
  );
};

export default Table;
