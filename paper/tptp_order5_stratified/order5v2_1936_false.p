% order5v2_1936  eq1=6293 eq2=14092  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(f(W,Z),Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(f(Y,Z),Z)),W)) )).
