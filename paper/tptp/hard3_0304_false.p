% hard3_0304  eq1=2859 eq2=1647  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(X,Y)),Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,Y),f(f(X,Y),X)) )).
