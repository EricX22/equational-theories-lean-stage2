% order5_0166  eq1=7898 eq2=33490  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(X,f(W,W)),Y))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(f(f(Z,Z),W),U)),Y) )).
