import DataSet from "../../../../business/domain/DataSet";
import di from "../../../../di";
import { createSlice } from "@reduxjs/toolkit";
import { GetDataSetsEvents } from "../events/GetDataSetsEvents";

export interface DataSetState {
  dataSets: DataSet[];
  isLoadingDataSet: boolean;
  error: string | null;
}

const initState: DataSetState = {
  dataSets: [],
  isLoadingDataSet: false,
  error: null,
};

const dataSetSlice = createSlice({
  name: "dataSet",
  initialState: initState,
  reducers: {},
  extraReducers: (builder) => {
    //get dataSets
    builder.addCase(
      di.GetDataSetsUseCase.getDataSets.pending,
      GetDataSetsEvents().handlePending
    );
    builder.addCase(
      di.GetDataSetsUseCase.getDataSets.fulfilled,
      GetDataSetsEvents().handleFulfilled
    );
    builder.addCase(
      di.GetDataSetsUseCase.getDataSets.rejected,
      GetDataSetsEvents().handleRejected
    );
  },
});

export default dataSetSlice.reducer;
