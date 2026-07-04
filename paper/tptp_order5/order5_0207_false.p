% order5_0207  eq1=31984 eq2=61180  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(f(Y,f(Y,Y)),Y)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,Y),Y) != f(f(X,f(X,Y)),X) )).
