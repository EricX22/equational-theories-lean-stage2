% order5v2_1275  eq1=5539 eq2=28949  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(U,f(X,U))))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(f(Y,Z),X),W),f(W,U)) )).
