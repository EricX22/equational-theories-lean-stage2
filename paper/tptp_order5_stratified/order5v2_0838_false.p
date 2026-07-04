% order5v2_0838  eq1=15089 eq2=17702  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),f(X,Z)),Y)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,Z),f(Z,f(W,f(W,U)))) )).
