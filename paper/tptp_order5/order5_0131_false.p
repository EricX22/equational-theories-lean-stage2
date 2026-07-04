% order5_0131  eq1=15022 eq2=5517  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),f(Y,Y)),X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(W,f(W,f(Y,W))))) )).
