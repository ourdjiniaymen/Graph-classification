import { createAsyncThunk } from "@reduxjs/toolkit";
import MainNetworkDataSource from "../datasource/network/MainNetworkDataSource";
import RunClassification from "../domain/RunClassification";
import { handleUseCaseError } from "./HandleUseCaseException";

export default class RunClassificationUseCase {
  constructor(private readonly mainNetworkDataSource: MainNetworkDataSource) {}

  runClassification = createAsyncThunk(
    "classification/runClassificationUseCase",
    async (runClassificationData: RunClassification, thunkAPI) => {
      const { rejectWithValue } = thunkAPI;
      try {
        return await this.mainNetworkDataSource.runClassification(
          runClassificationData
        );
      } catch (error: unknown) {
        return rejectWithValue(handleUseCaseError(error));
      }
    }
  );
}
