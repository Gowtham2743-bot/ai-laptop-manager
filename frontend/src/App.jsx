import { useEffect, useState } from "react";
import axios from "axios";
import {
  HardDrive,
  Search,
  FileText,
  Film,
  Image,
  Trash2,
  FolderOpen,
  RefreshCw,
  ShieldCheck,
  Clock3,
  Settings,
  Send,
  Bot,
  User,
  Sparkles,
  Database,
  AlertTriangle,
  Copy,
  ShieldAlert,
  PackageOpen,
  CheckCircle,
  XCircle,
} from "lucide-react";
import "./App.css";

const API = "";

function formatSize(bytes) {
  if (!bytes || bytes <= 0) return "0 B";

  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let i = 0;

  while (value >= 1024 && i < units.length - 1) {
    value /= 1024;
    i++;
  }

  return `${value.toFixed(2)} ${units[i]}`;
}

function App() {
  const [messages, setMessages] = useState([
    {
      type: "bot",
      text:
        "👋 Welcome to AI Laptop Manager!\n\n" +
        "I can search files, check storage, find large files, " +
        "open files, clean temporary files and manage Downloads safely.",
    },
  ]);

  const [input, setInput] = useState("");
  const [storage, setStorage] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activePage, setActivePage] = useState("chat");

  const [searchResults, setSearchResults] = useState([]);
  const [recentFiles, setRecentFiles] = useState([]);
  const [largeFiles, setLargeFiles] = useState([]);
  const [oldFiles, setOldFiles] = useState([]);

  const [securityFiles, setSecurityFiles] = useState([]);
  const [duplicateGroups, setDuplicateGroups] = useState([]);

  const [cleanupInfo, setCleanupInfo] = useState(null);
  const [organizeFiles, setOrganizeFiles] = useState([]);

  const [notification, setNotification] = useState("");

  useEffect(() => {
    loadStorage();
  }, []);

  async function loadStorage() {
    try {
      const response = await axios.get(`${API}/storage`);
      setStorage(response.data);

      const low = response.data.find(
        (drive) => drive.free < 15 * 1024 ** 3
      );

      if (low) {
        setNotification(
          `⚠ ${low.drive} has only ${formatSize(low.free)} free`
        );
      } else {
        setNotification("");
      }
    } catch {
      setNotification("Backend is not connected");
    }
  }

  function addMessage(type, text) {
    setMessages((prev) => [...prev, { type, text }]);
  }

  async function sendCommand(command = input) {
    const text = command.trim();

    if (!text || loading) return;

    setInput("");
    addMessage("user", text);

    const lower = text.toLowerCase();

    if (
      lower === "storage" ||
      lower.includes("check storage") ||
      lower.includes("show storage")
    ) {
      setLoading(true);
      addMessage("bot", "💾 Checking your storage...");
      await loadStorage();
      setActivePage("storage");
      setLoading(false);
      return;
    }

    if (lower.includes("dashboard")) {
      setActivePage("storage");
      addMessage("bot", "📊 Opening your storage dashboard.");
      await loadStorage();
      return;
    }

    if (
      lower.includes("recent") ||
      lower.includes("recent files")
    ) {
      await loadRecentFiles();
      return;
    }

    if (
      lower.includes("large") ||
      lower.includes("big file") ||
      lower.includes("big files")
    ) {
      await loadLargeFiles();
      return;
    }

    if (
      lower.includes("duplicate") ||
      lower.includes("duplicates")
    ) {
      await loadDuplicates();
      return;
    }

    if (
      lower.includes("security") ||
      lower.includes("suspicious") ||
      lower.includes("virus")
    ) {
      await loadSecurity();
      return;
    }

    if (
      lower.includes("old files") ||
      lower.includes("old file")
    ) {
      await loadOldFiles();
      return;
    }

    if (
      lower.includes("cleanup") ||
      lower.includes("clean my laptop") ||
      lower.includes("clean laptop")
    ) {
      await showCleanup();
      return;
    }

    if (
      lower.includes("organize downloads") ||
      lower.includes("organise downloads")
    ) {
      await showOrganizer();
      return;
    }

    if (
      lower.startsWith("find ") ||
      lower.startsWith("search ") ||
      lower.startsWith("where is ")
    ) {
      const keyword = lower
        .replace(/^find\s+/, "")
        .replace(/^search\s+/, "")
        .replace(/^where is\s+/, "")
        .trim();

      await searchFiles(keyword);
      return;
    }

    if (lower.startsWith("open ")) {
      const keyword = text.substring(5).trim();
      await searchFiles(keyword, true);
      return;
    }

    addMessage(
      "bot",
      `🤖 I understood: "${text}"\n\n` +
        "Try:\n" +
        "• find resume\n" +
        "• find certificate\n" +
        "• open movie\n" +
        "• recent files\n" +
        "• large files\n" +
        "• duplicate files\n" +
        "• security scan\n" +
        "• old files\n" +
        "• clean my laptop\n" +
        "• organize downloads\n" +
        "• storage"
    );
  }

  async function searchFiles(keyword, autoOpen = false) {
    if (!keyword) {
      addMessage("bot", "Please enter a file name or keyword.");
      return;
    }

    setLoading(true);
    addMessage("bot", `🔎 Searching for "${keyword}"...`);

    try {
      const response = await axios.get(`${API}/search`, {
        params: { keyword },
      });

      const results = response.data.results || [];

      setSearchResults(results);
      setActivePage("search");

      if (results.length === 0) {
        addMessage("bot", `❌ No files found for "${keyword}".`);
      } else {
        addMessage(
          "bot",
          `✅ Found ${results.length} file(s) matching "${keyword}".`
        );

        if (autoOpen && results.length === 1) {
          await openFile(results[0].path);
        }
      }
    } catch {
      addMessage(
        "bot",
        "❌ Search failed. Make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  }

  async function openFile(path) {
    try {
      await axios.get(`${API}/open`, {
        params: { path },
      });

      addMessage("bot", `📂 Opened:\n${path}`);
    } catch {
      addMessage("bot", "❌ Could not open that file.");
    }
  }

  async function openFolder(path) {
    try {
      await axios.get(`${API}/open-folder`, {
        params: { path },
      });
    } catch {
      addMessage("bot", "❌ Could not open the folder.");
    }
  }

  async function loadRecentFiles() {
    setLoading(true);
    addMessage("bot", "🕘 Finding recently modified files...");

    try {
      const response = await axios.get(`${API}/recent`);

      setRecentFiles(response.data.results || []);
      setActivePage("recent");
    } catch {
      addMessage("bot", "❌ Could not load recent files.");
    } finally {
      setLoading(false);
    }
  }

  async function loadLargeFiles() {
    setLoading(true);
    addMessage("bot", "📦 Finding large files...");

    try {
      const response = await axios.get(`${API}/large-files`);

      setLargeFiles(response.data.results || []);
      setActivePage("large");
    } catch {
      addMessage("bot", "❌ Could not load large files.");
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // SMART CLEANUP
  // =====================================================

  async function showCleanup() {
    setLoading(true);
    addMessage("bot", "🧹 Checking safe cleanup options...");

    try {
      const response = await axios.get(
        `${API}/cleanup-recommendations`
      );

      const recommendations =
        response.data.recommendations || [];

      setCleanupInfo(recommendations);

      if (recommendations.length === 0) {
        addMessage(
          "bot",
          "✅ Your safe cleanup areas look good. Nothing significant to clean."
        );
      } else {
        addMessage(
          "bot",
          `🧹 I found ${recommendations.length} cleanup option(s). Review them on the Cleanup page.`
        );
      }

      setActivePage("cleanup");
    } catch {
      addMessage(
        "bot",
        "❌ Could not check cleanup recommendations."
      );
    } finally {
      setLoading(false);
    }
  }

  async function performCleanup() {
    const confirmed = window.confirm(
      "Proceed with safe cleanup?\n\n" +
        "This will clean temporary files and empty the Recycle Bin.\n\n" +
        "Downloads, Documents, Desktop and project folders will NOT be deleted."
    );

    if (!confirmed) return;

    setLoading(true);
    addMessage("bot", "🧹 Cleaning safe temporary files...");

    let totalFreed = 0;

    try {
      const tempResponse = await axios.post(
        `${API}/cleanup/temp`
      );

      totalFreed += tempResponse.data.freed || 0;

      addMessage(
        "bot",
        `✅ Temporary cleanup completed.\nFreed: ${formatSize(
          tempResponse.data.freed || 0
        )}`
      );

      const recycleResponse = await axios.post(
        `${API}/cleanup/recycle-bin`
      );

      if (recycleResponse.data.success) {
        addMessage(
          "bot",
          "♻️ Recycle Bin emptied successfully."
        );
      }

      await loadStorage();
      await showCleanup();
    } catch {
      addMessage(
        "bot",
        "❌ Cleanup could not be completed."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // ORGANIZE DOWNLOADS
  // =====================================================

  async function showOrganizer() {
    setLoading(true);
    addMessage("bot", "📁 Checking your Downloads folder...");

    try {
      const response = await axios.get(
        `${API}/organize-preview`
      );

      const files = response.data.results || [];

      setOrganizeFiles(files);
      setActivePage("organize");

      if (files.length === 0) {
        addMessage(
          "bot",
          "✅ No files need automatic organization in Downloads."
        );
      } else {
        addMessage(
          "bot",
          `📁 Found ${files.length} file(s) that can be organized.`
        );
      }
    } catch {
      addMessage(
        "bot",
        "❌ Could not analyze Downloads."
      );
    } finally {
      setLoading(false);
    }
  }

  async function performOrganization() {
    const confirmed = window.confirm(
      "Organize these Downloads files?\n\n" +
        "Files will be moved into category folders such as Movies, Documents, Images, Audio, Archives and Software.\n\n" +
        "Your project folders will not be touched."
    );

    if (!confirmed) return;

    setLoading(true);
    addMessage(
      "bot",
      "📁 Organizing your Downloads..."
    );

    try {
      const response = await axios.post(
        `${API}/organize-downloads`
      );

      addMessage(
        "bot",
        `✅ Organization completed.\nMoved ${response.data.count || 0} file(s).`
      );

      await showOrganizer();
    } catch {
      addMessage(
        "bot",
        "❌ Downloads organization failed."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // SECURITY
  // =====================================================

  async function loadSecurity() {
    setLoading(true);
    addMessage(
      "bot",
      "🛡️ Scanning executable and script files..."
    );

    try {
      const response = await axios.get(
        `${API}/security`
      );

      setSecurityFiles(
        response.data.results || []
      );

      setActivePage("security");

      addMessage(
        "bot",
        `🛡️ Security check completed. Found ${
          response.data.count || 0
        } file(s) requiring review.`
      );
    } catch {
      addMessage(
        "bot",
        "❌ Security scan failed."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // DUPLICATES
  // =====================================================

  async function loadDuplicates() {
    setLoading(true);
    addMessage(
      "bot",
      "♻️ Searching for duplicate files..."
    );

    try {
      const response = await axios.get(
        `${API}/duplicates`
      );

      setDuplicateGroups(
        response.data.groups || []
      );

      setActivePage("duplicates");

      addMessage(
        "bot",
        `♻️ Duplicate scan completed. Found ${
          response.data.count || 0
        } duplicate group(s).`
      );
    } catch {
      addMessage(
        "bot",
        "❌ Duplicate scan failed."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // OLD FILES
  // =====================================================

  async function loadOldFiles() {
    setLoading(true);
    addMessage(
      "bot",
      "🕰️ Finding files older than one year..."
    );

    try {
      const response = await axios.get(
        `${API}/old-files`
      );

      setOldFiles(
        response.data.results || []
      );

      setActivePage("old");

      addMessage(
        "bot",
        `🕰️ Found ${response.data.count || 0} old file(s) for review.`
      );
    } catch {
      addMessage(
        "bot",
        "❌ Could not load old files."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // FILE CARD
  // =====================================================

  function FileCard({ file }) {
    const extension =
      file.type?.toLowerCase() || "";

    return (
      <div className="file-card">
        <div className="file-icon">
          {[".mp4", ".mkv", ".avi", ".mov"].some(
            (x) => extension.includes(x)
          ) ? (
            <Film size={25} />
          ) : [".jpg", ".jpeg", ".png", ".gif"].some(
              (x) => extension.includes(x)
            ) ? (
            <Image size={25} />
          ) : (
            <FileText size={25} />
          )}
        </div>

        <div className="file-info">
          <h3>{file.name}</h3>

          <p>{file.path}</p>

          <div className="file-meta">
            <span>
              {formatSize(file.size)}
            </span>

            <span>
              {file.type || "File"}
            </span>

            {file.mtime && (
              <span>
                {new Date(
                  file.mtime * 1000
                ).toLocaleString()}
              </span>
            )}
          </div>
        </div>

        <div className="file-actions">
          <button
            className="primary-btn"
            onClick={() =>
              openFile(file.path)
            }
          >
            <FolderOpen size={16} />
            Open
          </button>

          <button
            className="secondary-btn"
            onClick={() =>
              openFolder(file.path)
            }
          >
            Folder
          </button>
        </div>
      </div>
    );
  }

  // =====================================================
  // STORAGE PAGE
  // =====================================================

  function StoragePage() {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>Storage Dashboard</h1>
            <p>
              Monitor your C: and D: drives.
            </p>
          </div>

          <button
            className="secondary-btn"
            onClick={loadStorage}
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        <div className="storage-grid">
          {storage.map((drive) => {
            const low =
              drive.free <
              15 * 1024 ** 3;

            const warning =
              drive.free <
                25 * 1024 ** 3 &&
              !low;

            return (
              <div
                className="storage-card"
                key={drive.drive}
              >
                <div className="storage-header">
                  <div>
                    <h2>
                      <HardDrive size={20} />
                      {drive.drive}
                    </h2>

                    <p>
                      {drive.used_percent}% used
                    </p>
                  </div>

                  {low ? (
                    <AlertTriangle className="danger-icon" />
                  ) : warning ? (
                    <AlertTriangle className="warning-icon" />
                  ) : (
                    <ShieldCheck className="safe-icon" />
                  )}
                </div>

                <div className="storage-bar">
                  <div
                    className={`storage-fill ${
                      low
                        ? "danger"
                        : warning
                        ? "warning"
                        : ""
                    }`}
                    style={{
                      width: `${drive.used_percent}%`,
                    }}
                  />
                </div>

                <div className="storage-numbers">
                  <span>
                    Used
                    <b>
                      {formatSize(
                        drive.used
                      )}
                    </b>
                  </span>

                  <span>
                    Free
                    <b>
                      {formatSize(
                        drive.free
                      )}
                    </b>
                  </span>

                  <span>
                    Total
                    <b>
                      {formatSize(
                        drive.total
                      )}
                    </b>
                  </span>
                </div>

                <div
                  className={`storage-status ${
                    low
                      ? "danger-text"
                      : warning
                      ? "warning-text"
                      : ""
                  }`}
                >
                  {low
                    ? "Very low free space"
                    : warning
                    ? "Free space is getting low"
                    : "Storage level is good"}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // =====================================================
  // CLEANUP PAGE
  // =====================================================

  function CleanupPage() {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>Smart Cleanup</h1>
            <p>
              Safe cleanup recommendations.
            </p>
          </div>

          <button
            className="secondary-btn"
            onClick={showCleanup}
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {cleanupInfo?.length === 0 ? (
          <div className="empty">
            <CheckCircle size={42} />
            <h2>
              Nothing significant to clean
            </h2>
          </div>
        ) : (
          <>
            <div className="file-list">
              {(cleanupInfo || []).map(
                (item) => (
                  <div
                    className="file-card"
                    key={item.id}
                  >
                    <div className="file-icon">
                      <Trash2 size={25} />
                    </div>

                    <div className="file-info">
                      <h3>
                        {item.name}
                      </h3>

                      <p>
                        {item.description}
                      </p>

                      <div className="file-meta">
                        <span>
                          {item.size_text}
                        </span>

                        <span>
                          {item.safe
                            ? "Safe cleanup"
                            : "Manual review"}
                        </span>
                      </div>
                    </div>

                    {item.safe && (
                      <CheckCircle
                        className="safe-icon"
                        size={23}
                      />
                    )}
                  </div>
                )
              )}
            </div>

            {cleanupInfo?.some(
              (x) => x.safe
            ) && (
              <div
                style={{
                  marginTop: "20px",
                }}
              >
                <button
                  className="primary-btn"
                  onClick={
                    performCleanup
                  }
                >
                  <Trash2 size={17} />
                  Clean Safe Files
                </button>
              </div>
            )}
          </>
        )}
      </div>
    );
  }

  // =====================================================
  // ORGANIZE PAGE
  // =====================================================

  function OrganizePage() {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>
              Organize Downloads
            </h1>

            <p>
              Review files before moving them.
            </p>
          </div>

          <button
            className="secondary-btn"
            onClick={
              showOrganizer
            }
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {organizeFiles.length === 0 ? (
          <div className="empty">
            <CheckCircle size={42} />
            <h2>
              No files need organizing
            </h2>
          </div>
        ) : (
          <>
            <div className="file-list">
              {organizeFiles.map(
                (file, index) => (
                  <div
                    className="file-card"
                    key={`${file.path}-${index}`}
                  >
                    <div className="file-icon">
                      <PackageOpen
                        size={25}
                      />
                    </div>

                    <div className="file-info">
                      <h3>
                        {file.name}
                      </h3>

                      <p>
                        Downloads →{" "}
                        {file.category}
                      </p>

                      <div className="file-meta">
                        <span>
                          {file.size_text}
                        </span>

                        <span>
                          {file.category}
                        </span>
                      </div>
                    </div>
                  </div>
                )
              )}
            </div>

            <div
              style={{
                marginTop: "20px",
              }}
            >
              <button
                className="primary-btn"
                onClick={
                  performOrganization
                }
              >
                <FolderOpen size={17} />
                Organize Files
              </button>
            </div>
          </>
        )}
      </div>
    );
  }

  // =====================================================
  // SECURITY PAGE
  // =====================================================

  function SecurityPage() {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>
              Security Check
            </h1>

            <p>
              Executable and script files
              requiring review.
            </p>
          </div>

          <button
            className="secondary-btn"
            onClick={loadSecurity}
          >
            <RefreshCw size={16} />
            Scan Again
          </button>
        </div>

        <div
          style={{
            padding: "14px 16px",
            marginBottom: "18px",
            borderRadius: "10px",
            border: "1px solid #44391f",
            background: "#211d14",
            color: "#dcb968",
            fontSize: "12px",
          }}
        >
          <ShieldAlert
            size={16}
            style={{
              verticalAlign: "middle",
              marginRight: "7px",
            }}
          />
          This is a file-type checker, not
          an antivirus scanner. Files are
          only flagged for review.
        </div>

        {securityFiles.length === 0 ? (
          <div className="empty">
            <CheckCircle size={42} />
            <h2>
              No suspicious file types found
            </h2>
          </div>
        ) : (
          <div className="file-list">
            {securityFiles.map(
              (file, index) => (
                <div
                  className="file-card"
                  key={`${file.path}-${index}`}
                >
                  <div className="file-icon">
                    <ShieldAlert
                      size={25}
                    />
                  </div>

                  <div className="file-info">
                    <h3>
                      {file.name}
                    </h3>

                    <p>
                      {file.path}
                    </p>

                    <div className="file-meta">
                      <span>
                        {formatSize(
                          file.size
                        )}
                      </span>

                      <span>
                        {file.type}
                      </span>

                      <span>
                        Review
                      </span>
                    </div>
                  </div>

                  <button
                    className="secondary-btn"
                    onClick={() =>
                      openFolder(
                        file.path
                      )
                    }
                  >
                    Folder
                  </button>
                </div>
              )
            )}
          </div>
        )}
      </div>
    );
  }

  // =====================================================
  // DUPLICATE PAGE
  // =====================================================

  function DuplicatePage() {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>
              Duplicate Files
            </h1>

            <p>
              Identical files grouped by
              content.
            </p>
          </div>

          <button
            className="secondary-btn"
            onClick={
              loadDuplicates
            }
          >
            <RefreshCw size={16} />
            Scan Again
          </button>
        </div>

        {duplicateGroups.length === 0 ? (
          <div className="empty">
            <CheckCircle size={42} />
            <h2>
              No duplicate groups found
            </h2>
          </div>
        ) : (
          <div className="file-list">
            {duplicateGroups.map(
              (group, index) => (
                <div
                  className="file-card"
                  key={index}
                  style={{
                    display: "block",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "12px",
                      marginBottom:
                        "12px",
                    }}
                  >
                    <div className="file-icon">
                      <Copy size={23} />
                    </div>

                    <div>
                      <h3
                        style={{
                          margin: 0,
                        }}
                      >
                        {group.count} identical
                        files
                      </h3>

                      <p
                        style={{
                          margin:
                            "5px 0 0",
                        }}
                      >
                        Potential wasted space:{" "}
                        {
                          group.wasted_text
                        }
                      </p>
                    </div>
                  </div>

                  {group.files.map(
                    (file, fileIndex) => (
                      <div
                        key={fileIndex}
                        style={{
                          padding:
                            "8px 0",
                          borderTop:
                            "1px solid #242c37",
                          fontSize:
                            "12px",
                          color:
                            "#8994a4",
                        }}
                      >
                        {file.path}
                      </div>
                    )
                  )}
                </div>
              )
            )}
          </div>
        )}
      </div>
    );
  }

  // =====================================================
  // CHAT PAGE
  // =====================================================

  function ChatPage() {
    return (
      <div className="chat-page">
        <div className="messages">
          {messages.map(
            (message, index) => (
              <div
                className={`message-row ${
                  message.type === "user"
                    ? "user-row"
                    : ""
                }`}
                key={index}
              >
                <div
                  className={`avatar ${
                    message.type ===
                    "user"
                      ? "user-avatar"
                      : ""
                  }`}
                >
                  {message.type ===
                  "user" ? (
                    <User size={18} />
                  ) : (
                    <Bot size={18} />
                  )}
                </div>

                <div
                  className={`message ${
                    message.type ===
                    "user"
                      ? "user-message"
                      : "bot-message"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            )
          )}

          {loading && (
            <div className="typing">
              <Sparkles size={15} />
              AI Laptop Manager is working...
            </div>
          )}
        </div>

        <div className="suggestions">
          {[
            "find resume",
            "storage",
            "recent files",
            "large files",
            "clean my laptop",
            "organize downloads",
          ].map((item) => (
            <button
              key={item}
              onClick={() =>
                sendCommand(item)
              }
            >
              {item}
            </button>
          ))}
        </div>

        <div className="chat-input">
          <input
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendCommand();
              }
            }}
            placeholder="Ask AI Laptop Manager..."
            disabled={loading}
          />

          <button
            onClick={() =>
              sendCommand()
            }
            disabled={loading}
          >
            <Send size={19} />
          </button>
        </div>
      </div>
    );
  }

  // =====================================================
  // RESULTS PAGE
  // =====================================================

  function ResultsPage({
    title,
    files,
  }) {
    return (
      <div className="page">
        <div className="page-title">
          <div>
            <h1>{title}</h1>
            <p>
              {files.length} result(s)
            </p>
          </div>
        </div>

        {files.length === 0 ? (
          <div className="empty">
            <Database size={42} />
            <h2>
              No files found
            </h2>
          </div>
        ) : (
          <div className="file-list">
            {files.map(
              (file, index) => (
                <FileCard
                  file={file}
                  key={`${file.path}-${index}`}
                />
              )
            )}
          </div>
        )}
      </div>
    );
  }

  // =====================================================
  // MAIN UI
  // =====================================================

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Bot size={25} />
          </div>

          <div>
            <h2>AI Laptop</h2>
            <span>Manager</span>
          </div>
        </div>

        <div className="nav-title">
          MANAGER
        </div>

        <button
          className={
            activePage === "chat"
              ? "nav active"
              : "nav"
          }
          onClick={() =>
            setActivePage("chat")
          }
        >
          <Bot size={18} />
          AI Chat
        </button>

        <button
          className={
            activePage === "storage"
              ? "nav active"
              : "nav"
          }
          onClick={() => {
            setActivePage("storage");
            loadStorage();
          }}
        >
          <HardDrive size={18} />
          Storage
        </button>

        <button
          className={
            activePage === "search"
              ? "nav active"
              : "nav"
          }
          onClick={() =>
            setActivePage("search")
          }
        >
          <Search size={18} />
          File Search
        </button>

        <button
          className={
            activePage === "recent"
              ? "nav active"
              : "nav"
          }
          onClick={
            loadRecentFiles
          }
        >
          <Clock3 size={18} />
          Recent Files
        </button>

        <button
          className={
            activePage === "large"
              ? "nav active"
              : "nav"
          }
          onClick={
            loadLargeFiles
          }
        >
          <Database size={18} />
          Large Files
        </button>

        <div className="nav-title">
          TOOLS
        </div>

        <button
          className={
            activePage === "cleanup"
              ? "nav active"
              : "nav"
          }
          onClick={
            showCleanup
          }
        >
          <Trash2 size={18} />
          Smart Cleanup
        </button>

        <button
          className={
            activePage === "organize"
              ? "nav active"
              : "nav"
          }
          onClick={
            showOrganizer
          }
        >
          <FolderOpen size={18} />
          Organize Downloads
        </button>

        <button
          className={
            activePage === "security"
              ? "nav active"
              : "nav"
          }
          onClick={
            loadSecurity
          }
        >
          <ShieldCheck size={18} />
          Security
        </button>

        <button
          className={
            activePage === "duplicates"
              ? "nav active"
              : "nav"
          }
          onClick={
            loadDuplicates
          }
        >
          <Copy size={18} />
          Duplicates
        </button>

        <button
          className={
            activePage === "old"
              ? "nav active"
              : "nav"
          }
          onClick={
            loadOldFiles
          }
        >
          <Clock3 size={18} />
          Old Files
        </button>

        <div className="sidebar-bottom">
          <div className="connection">
            <span className="online-dot" />
            Backend connected
          </div>

          <button className="nav">
            <Settings size={18} />
            Settings
          </button>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>
              AI Laptop Manager
            </h1>

            <p>
              Your local laptop assistant
            </p>
          </div>

          <div className="top-status">
            {notification && (
              <span className="notification">
                <AlertTriangle size={15} />
                {notification}
              </span>
            )}

            <button
              className="icon-btn"
              onClick={
                loadStorage
              }
              title="Refresh storage"
            >
              <RefreshCw size={18} />
            </button>
          </div>
        </header>

        <section className="content">
          {activePage ===
            "chat" && (
            <ChatPage />
          )}

          {activePage ===
            "storage" && (
            <StoragePage />
          )}

          {activePage ===
            "search" && (
            <ResultsPage
              title="File Search"
              files={
                searchResults
              }
            />
          )}

          {activePage ===
            "recent" && (
            <ResultsPage
              title="Recent Files"
              files={
                recentFiles
              }
            />
          )}

          {activePage ===
            "large" && (
            <ResultsPage
              title="Large Files"
              files={
                largeFiles
              }
            />
          )}

          {activePage ===
            "cleanup" && (
            <CleanupPage />
          )}

          {activePage ===
            "organize" && (
            <OrganizePage />
          )}

          {activePage ===
            "security" && (
            <SecurityPage />
          )}

          {activePage ===
            "duplicates" && (
            <DuplicatePage />
          )}

          {activePage ===
            "old" && (
            <ResultsPage
              title="Old Files"
              files={oldFiles}
            />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;