import {aE as V, r as $, w as J, J as c, o as m, c as b, g as n, F as T, h as S, a as e, d as s, t as w, q as K, aG as O, Q as i, K as x, a3 as C, A as y, bY as d, a2 as R, cj as Y, m as H, ch as W, c0 as X, ab as D, ac as Z, x as _, k as E, b as M, f as ee, j as B, ck as ae, z as q, ar as te, as as h, at as se, au as u, n as ne, C as oe, p as le, i as re, cl as ie, cm as de} from "./vendor.js";
import {h as ce, i as ue, j as pe} from "./e.QBar.js";
import {D as p} from "./DocCode.js";
import {_ as P} from "./e.AppFullscreen.js";
import {D as me} from "./DocPage.js";
import "./CopyButton.js";
import "./index.js";
const ge = {
    id: "theme-picker"
}
  , fe = {
    class: "row items-stretch"
}
  , ye = {
    class: "theme-picker__colors flex q-gutter-sm"
}
  , he = {
    class: "text-weight-light"
}
  , _e = {
    class: "text-capitalize"
}
  , ve = {
    class: "theme-picker__content col"
}
  , ke = {
    class: "q-px-md q-py-lg"
}
  , $e = {
    class: "row q-col-gutter-md"
}
  , be = {
    class: "text-h6 row no-wrap items-center"
}
  , we = {
    class: "ellipsis text-capitalize"
}
  , xe = {
    class: "col-12 row items-center justify-end q-gutter-md"
}
  , Ce = {
    __name: "ThemePicker",
    setup(z) {
        const {luminosity: v} = de
          , a = V({
            primary: "#1976d2",
            secondary: "#26A69A",
            accent: "#9C27B0",
            dark: "#1d1d1d",
            "dark-page": "#121212",
            positive: "#21BA45",
            negative: "#C10015",
            info: "#31CCEC",
            warning: "#F2C037"
        })
          , l = V({
            primary: !0,
            secondary: !0,
            accent: !0,
            dark: !0,
            "dark-page": !0,
            positive: !0,
            negative: !0,
            info: !1,
            warning: !1
        })
          , g = $(!1)
          , k = $(!1)
          , f = $("sass");
        function I(r, o) {
            ie(r, o, document.getElementById("theme-picker")),
            l[r] = v(o) <= .4
        }
        const Q = ["primary", "secondary", "accent", "dark", "dark-page", "positive", "negative", "info", "warning"];
        Q.forEach(r=>{
            J(()=>a[r], o=>{
                I(r, o)
            }
            )
        }
        );
        const U = c(()=>g.value === !0 ? "theme-picker__bg-dark text-white" : "bg-white text-black")
          , A = c(()=>`// src/css/quasar.variables.sass

$primary   : ${a.primary}
$secondary : ${a.secondary}
$accent    : ${a.accent}

$dark      : ${a.dark}
$dark-page : ${a["dark-page"]}

$positive  : ${a.positive}
$negative  : ${a.negative}
$info      : ${a.info}
$warning   : ${a.warning}`)
          , j = c(()=>`// src/css/quasar.variables.scss

$primary   : ${a.primary};
$secondary : ${a.secondary};
$accent    : ${a.accent};

$dark      : ${a.dark};
$dark-page : ${a["dark-page"]};

$positive  : ${a.positive};
$negative  : ${a.negative};
$info      : ${a.info};
$warning   : ${a.warning};`)
          , L = c(()=>`// quasar.config file

return {
  framework: {
    config: {
      brand: {
        primary: '${a.primary}',
        secondary: '${a.secondary}',
        accent: '${a.accent}',

        dark: '${a.dark}',
        'dark-page': '${a["dark-page"]}',

        positive: '${a.positive}',
        negative: '${a.negative}',
        info: '${a.info}',
        warning: '${a.warning}'
      }
    }
  }
}`)
          , F = c(()=>`app.use(Quasar, {
  config: {
    brand: {
      primary: '${a.primary}',
      secondary: '${a.secondary}',
      accent: '${a.accent}',

      dark: '${a.dark}',
      'dark-page': '${a["dark-page"]}',

      positive: '${a.positive}',
      negative: '${a.negative}',
      info: '${a.info}',
      warning: '${a.warning}'
    }
  }
}`)
          , N = ["secondary", "dark", "positive", "negative", "info", "warning"];
        return (r,o)=>(m(),
        b("div", ge, [n("div", fe, [n("div", ye, [(m(),
        b(T, null, S(Q, t=>e(i, {
            key: `picker-${t}`,
            color: t,
            "text-color": l[t] === !0 ? "white" : "black",
            "no-caps": "",
            glossy: "",
            unelevated: ""
        }, {
            default: s(()=>[n("div", he, [n("div", _e, w(t), 1), n("div", null, w(a[t]), 1)]), e(K, {
                anchor: "top start",
                self: "top start"
            }, {
                default: s(()=>[e(O, {
                    modelValue: a[t],
                    "onUpdate:modelValue": G=>a[t] = G
                }, null, 8, ["modelValue", "onUpdate:modelValue"])]),
                _: 2
            }, 1024)]),
            _: 2
        }, 1032, ["color", "text-color"])), 64))]), n("div", ve, [n("div", {
            class: x(["relative-position fit rounded-borders shadow-2 bg-white overflow-hidden", U.value])
        }, [n("div", {
            class: x(`bg-primary text-${l.primary === !0 ? "white shadow-2" : "black"}`)
        }, [e(R, {
            dense: "",
            dark: l.primary
        }, {
            default: s(()=>[e(C), e(y, {
                class: "q-mr-xs",
                name: d(ce),
                size: "12px",
                style: {
                    opacity: "0.5"
                }
            }, null, 8, ["name"]), e(y, {
                class: "q-mr-xs",
                name: d(ue),
                size: "12px",
                style: {
                    opacity: "0.5"
                }
            }, null, 8, ["name"]), e(y, {
                class: "q-mr-sm rotate-90",
                name: d(pe),
                size: "12px",
                style: {
                    opacity: "0.5"
                }
            }, null, 8, ["name"])]),
            _: 1
        }, 8, ["dark"]), e(D, null, {
            default: s(()=>[e(i, {
                flat: "",
                dense: "",
                round: "",
                icon: d(Y)
            }, null, 8, ["icon"]), e(C), e(H, {
                class: "q-mr-sm",
                dense: "",
                modelValue: g.value,
                "onUpdate:modelValue": o[0] || (o[0] = t=>g.value = t),
                dark: l.primary,
                color: "red",
                label: "Dark page"
            }, null, 8, ["modelValue", "dark"]), e(i, {
                flat: "",
                dense: "",
                round: "",
                icon: d(W)
            }, null, 8, ["icon"]), e(i, {
                flat: "",
                dense: "",
                round: "",
                icon: d(X)
            }, null, 8, ["icon"])]),
            _: 1
        }), e(D, {
            inset: ""
        }, {
            default: s(()=>[e(Z, null, {
                default: s(()=>[_("Quasar")]),
                _: 1
            })]),
            _: 1
        })], 2), n("div", ke, [n("div", $e, [(m(),
        b(T, null, S(N, t=>n("div", {
            class: "col-12 col-sm-6 col-md-4 col-lg-3",
            key: `card-${t}`
        }, [e(B, {
            flat: "",
            class: x(`bg-${t} text-${l[t] === !0 ? "white" : "black"}`)
        }, {
            default: s(()=>[e(E, null, {
                default: s(()=>[n("div", be, [n("div", we, w(t), 1), e(C), t !== "secondary" && t !== "dark" ? (m(),
                M(y, {
                    key: 0,
                    name: r.$q.iconSet.type[t],
                    size: "24px"
                }, null, 8, ["name"])) : ee("", !0)])]),
                _: 2
            }, 1024), e(E, null, {
                default: s(()=>[_("Lorem, ipsum dolor sit amet consectetur adipisicing elit.")]),
                _: 1
            })]),
            _: 2
        }, 1032, ["class"])])), 64))]), e(i, {
            class: "absolute",
            fab: "",
            icon: d(ae),
            color: "accent",
            "text-color": l.accent === !0 ? "white" : "black",
            style: {
                bottom: "16px",
                right: "16px"
            }
        }, null, 8, ["icon", "text-color"])])], 2)])]), e(q, {
            class: "q-mt-lg q-mb-sm"
        }), n("div", xe, [e(i, {
            class: "call-to-action-btn",
            "no-caps": "",
            padding: "8px 16px",
            label: "Export",
            onClick: o[1] || (o[1] = t=>k.value = !0)
        })]), e(re, {
            modelValue: k.value,
            "onUpdate:modelValue": o[4] || (o[4] = t=>k.value = t)
        }, {
            default: s(()=>[e(B, null, {
                default: s(()=>[e(te, {
                    class: "theme-picker__tabs text-grey-7",
                    modelValue: f.value,
                    "onUpdate:modelValue": o[2] || (o[2] = t=>f.value = t),
                    "active-color": "brand-primary",
                    align: "justify"
                }, {
                    default: s(()=>[e(h, {
                        name: "sass",
                        "no-caps": "",
                        label: "Sass"
                    }), e(h, {
                        name: "scss",
                        "no-caps": "",
                        label: "SCSS"
                    }), e(h, {
                        name: "quasar-cli",
                        "no-caps": "",
                        label: "Quasar CLI"
                    }), e(h, {
                        name: "umd",
                        "no-caps": "",
                        label: "Vite / UMD / Vue CLI"
                    })]),
                    _: 1
                }, 8, ["modelValue"]), e(q), e(se, {
                    modelValue: f.value,
                    "onUpdate:modelValue": o[3] || (o[3] = t=>f.value = t),
                    animated: ""
                }, {
                    default: s(()=>[e(u, {
                        class: "q-pa-none",
                        name: "sass"
                    }, {
                        default: s(()=>[e(p, {
                            copy: "",
                            code: A.value
                        }, null, 8, ["code"])]),
                        _: 1
                    }), e(u, {
                        class: "q-pa-none",
                        name: "scss"
                    }, {
                        default: s(()=>[e(p, {
                            copy: "",
                            code: j.value
                        }, null, 8, ["code"])]),
                        _: 1
                    }), e(u, {
                        class: "q-pa-none",
                        name: "quasar-cli"
                    }, {
                        default: s(()=>[e(p, {
                            copy: "",
                            code: L.value
                        }, null, 8, ["code"])]),
                        _: 1
                    }), e(u, {
                        class: "q-pa-none",
                        name: "umd"
                    }, {
                        default: s(()=>[e(p, {
                            copy: "",
                            code: F.value
                        }, null, 8, ["code"])]),
                        _: 1
                    }), e(u, {
                        class: "q-pa-none",
                        name: "vue-cli"
                    }, {
                        default: s(()=>[e(p, {
                            copy: "",
                            code: r.vueCliExport
                        }, null, 8, ["code"])]),
                        _: 1
                    })]),
                    _: 1
                }, 8, ["modelValue"]), e(q), e(ne, {
                    align: "right"
                }, {
                    default: s(()=>[le(e(i, {
                        class: "call-to-action-btn",
                        "no-caps": "",
                        padding: "8px 16px",
                        label: "Close"
                    }, null, 512), [[oe]])]),
                    _: 1
                })]),
                _: 1
            })]),
            _: 1
        }, 8, ["modelValue"])]))
    }
}
  , qe = P(Ce, [["__file", "ThemePicker.vue"]])
  , Qe = n("p", null, "One of the most important parts of a website/app is to build a brand for it. First step is to choose the brand colors that you are going to use and this is what the tool below helps you with.", -1)
  , Ve = n("p", null, [_("Click on the colored buttons besides the layout below and when you are ready, hit the "), n("code", {
    class: "doc-token"
}, "Export"), _(" button at the bottom.")], -1)
  , Te = {
    __name: "theme-builder",
    setup(z) {
        const v = [{
            name: "Dark Mode",
            category: "Style & Identity",
            path: "/style/dark-mode"
        }]
          , a = [{
            name: "Color Palette",
            category: "Style & Identity",
            path: "/style/color-palette",
            classes: "doc-page__related--left"
        }, {
            name: "Dark Mode",
            category: "Style & Identity",
            path: "/style/dark-mode",
            classes: "doc-page__related--right"
        }];
        return (l,g)=>(m(),
        M(me, {
            title: "Theme Builder",
            desc: "Theme builder for a Quasar app with which you can play with the brand colors.",
            heading: "",
            "edit-link": "style/theme-builder/theme-builder",
            related: v,
            nav: a
        }, {
            default: s(()=>[Qe, Ve, e(qe, {
                class: "q-py-lg"
            })]),
            _: 1
        }))
    }
}
  , Ie = P(Te, [["__file", "theme-builder.md"]]);
export {Ie as default};
