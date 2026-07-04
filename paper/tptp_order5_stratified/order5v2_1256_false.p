% order5v2_1256  eq1=20230 eq2=5544  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Z,Z)),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(Z,f(W,f(U,f(Y,W))))) )).
