% order5_0192  eq1=5017 eq2=41620  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(Z,f(Z,f(Z,W))))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(Y,f(Y,f(X,f(X,Z)))) )).
