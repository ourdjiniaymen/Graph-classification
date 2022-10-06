import { createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import DataSet from "../../../../business/domain/DataSet";
import di from "../../../../di";
import { DataSetState } from "../slices/DataSetSlice";

export const GetDataSetsEvents = () => {
  const getDataSetsEvent = createAsyncThunk(
    "dataSet/getDataSetsEvent",
    async (_, thunkAPI) => {
      const { dispatch } = thunkAPI;
      dispatch(di.GetDataSetsUseCase.getDataSets());
    }
  );

  const handlePending = (state: DataSetState) => {
    state.isLoadingDataSet = true;
    state.error = null;
  };

  const handleFulfilled = (
    state: DataSetState,
    action: PayloadAction<DataSet[]>
  ) => {
    state.isLoadingDataSet = false;
    state.dataSets = action.payload;
  };

  const handleRejected = (
    state: DataSetState,
    action: PayloadAction<unknown>
  ) => {
    state.isLoadingDataSet = false;
    state.error = action.payload as string;
  };
  return {
    getDataSetsEvent,
    handlePending,
    handleFulfilled,
    handleRejected,
  };
};
