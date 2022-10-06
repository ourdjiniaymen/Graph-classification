import React from "react";
import TextField from "@mui/material/TextField";

interface Props {
  label: string;
  value: string;
  onChange: (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void;
}

const NumberField = ({ label, value, onChange }: Props) => {
  return (
    <TextField
      label={label}
      value={value}
      onChange={onChange}
      type="number"
      InputProps={{ inputProps: { min: 0 } }}
      InputLabelProps={{
        shrink: true,
      }}
      variant="outlined"
      sx={{
        m: 1,
        minWidth: 400,
        padding: "10px",
      }}
    />
  );
};

export default NumberField;
