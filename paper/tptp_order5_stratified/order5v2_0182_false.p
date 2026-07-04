% order5v2_0182  eq1=42254 eq2=52400  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(Z,f(W,f(W,X)))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(X,Y) != f(f(f(X,f(Z,W)),W),U) )).
