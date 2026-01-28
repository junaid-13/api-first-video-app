import React from "react";
import { View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { getStreamUrl } from "../services/api";
import { WebView } from "react-native-webview";

type Props = NativeStackScreenProps<RootStackParamList, "VideoPlayer">;

export default function VideoPlayerScreen({ route }: Props) {
  const { videoId, token } = route.params;

  const streamUrl = getStreamUrl(videoId);

  return (
    <View style={{ flex: 1 }}>
      <WebView
        source={{
          uri: streamUrl,
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }}
      />
    </View>
  );
}
