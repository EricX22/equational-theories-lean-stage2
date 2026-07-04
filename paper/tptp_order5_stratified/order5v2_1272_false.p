% order5v2_1272  eq1=5105 eq2=7673  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Y,f(Y,f(Z,W))))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(Y,f(X,f(f(Z,f(W,W)),U))) )).
