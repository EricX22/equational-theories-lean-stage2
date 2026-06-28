% hard3_0043  eq1=259 eq2=2684  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,X),Y),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,Y),f(Z,Y)),Y) )).
