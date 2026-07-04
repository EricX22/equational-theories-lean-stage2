% order5_0168  eq1=12402 eq2=37595  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),Y),f(W,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,f(Y,f(Z,Y))),Y),Z) )).
