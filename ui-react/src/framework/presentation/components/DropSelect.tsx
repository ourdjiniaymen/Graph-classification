import React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

interface Props {
  label: string;
  textHelper: string;
  value: string;
  handleChange: (event: SelectChangeEvent) => void;
  selectOptions: { value: string; label: string }[];
}

const DropSelect = ({
  label,
  textHelper,
  value,
  handleChange,
  selectOptions,
}: Props) => {
  return (
    <div>
      <FormControl
        sx={{
          m: 1,
          minWidth: 400,
          margin: "auto",
          padding: "10px",
        }}
      >
        <InputLabel id="demo-simple-select-helper-label">{label}</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={value}
          label={label}
          onChange={handleChange}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          {selectOptions.map((option) => (
            <MenuItem value={option.value}>{option.label}</MenuItem>
          ))}
        </Select>
        <FormHelperText>{textHelper}</FormHelperText>
      </FormControl>
    </div>
  );
};

export default DropSelect;
