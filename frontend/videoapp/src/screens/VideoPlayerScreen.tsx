import React from "react";
import { View, Text } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "VideoPlayer">;

const VideoPlayerScreen: React.FC<Props> = ({ route }) => {
  const { videoId } = route.params;

  return (
    <View>
      <Text>Playing video: {videoId}</Text>
    </View>
  );
};

export default VideoPlayerScreen;
