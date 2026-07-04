% order5v2_0342  eq1=16546 eq2=13124  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),Y),Y),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(X,f(Y,W))),Z)) )).
